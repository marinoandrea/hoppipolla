use std::{collections::HashMap, net::SocketAddr, sync::Arc};

use lazy_static::lazy_static;
use tokio::sync::{Mutex, RwLock};
use tonic::{transport::Channel, Request, Response, Status};

use crate::db::PolicyDb;
use crate::entities::{Issuer, IssuerId, MetaPolicy, Policy, PolicyId};
use crate::nip_proxy::nip_proxy_client::NipProxyClient;
use crate::nip_proxy::{self as nippb};
use crate::path_analyzer::path_analyzer_client::PathAnalyzerClient;
use crate::policy_manager::policy_manager_server::PolicyManager;
use crate::policy_manager::{self as pb};
use crate::reasoner::{self, ReasonerError};

pub struct Service {
    config: crate::Config,
    db: PolicyDb,
    meta_policy: Option<MetaPolicy>,
    policies: Arc<RwLock<HashMap<PolicyId, Policy>>>,
    issuers: Arc<RwLock<HashMap<IssuerId, Issuer>>>,
    nip_proxy: Option<NipProxyClient<Channel>>,
}

struct ClientHandle {
    stale: bool,
    addr: SocketAddr,
    chan: PathAnalyzerClient<Channel>,
}

impl ClientHandle {
    async fn refresh(&mut self) -> Result<(), Status> {
        if self.stale {
            self.chan.refresh(Request::new(())).await?;
            self.stale = false;
        }
        Ok(())
    }
}

lazy_static! {
    static ref CLIENTS: Mutex<Vec<ClientHandle>> = Mutex::new(Vec::default());
}

/// Retries client refresh RPCs until they are not stale anymore
pub async fn run_broadcast_daemon() -> Result<(), tonic::transport::Error> {
    loop {
        let mut clients = CLIENTS.lock().await;
        for client in clients.iter_mut() {
            if client.refresh().await.is_err() {
                log::error!("failed to refresh client {}", client.addr)
            }
        }
        tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
    }
}

impl Service {
    async fn refresh(&self) -> Result<(), Status> {
        let mut clients = CLIENTS.lock().await;

        // TODO(andrea): parallelize
        for client in clients.iter_mut() {
            client.stale = true;
            if let Err(e) = client.refresh().await {
                return Err(Status::internal(e.message()));
            }
        }

        Ok(())
    }

    pub async fn with_config(config: crate::Config) -> Self {
        let db = PolicyDb::new(&config.db_uri, config.db_max_conns).await;

        let policies = Arc::new(RwLock::new(
            db.load_policies()
                .await
                .into_iter()
                .map(|p| (p.id(), p))
                .collect::<HashMap<_, _>>(),
        ));

        let issuers = Arc::new(RwLock::new(
            db.load_issuers()
                .await
                .into_iter()
                .map(|i| (i.id(), i))
                .collect::<HashMap<_, _>>(),
        ));

        let meta_policy = db.load_meta_policy().await;

        Self {
            config,
            db,
            policies,
            issuers,
            meta_policy,
            nip_proxy: None, // needs to be initialized at startup
        }
    }

    pub async fn init(&mut self) -> Result<(), Status> {
        self.nip_proxy = Some(
            NipProxyClient::connect(self.config.nip_proxy_addr.to_string())
                .await
                .map_err(|e| Status::unknown(e.to_string()))?,
        );
        Ok(())
    }
}

#[tonic::async_trait]
impl PolicyManager for Service {
    async fn create_policy(
        &self,
        request: tonic::Request<pb::CreatePolicyRequest>,
    ) -> std::result::Result<Response<pb::CreatePolicyResponse>, Status> {
        let req = request.get_ref().clone();
        let mut res = pb::CreatePolicyResponse::default();

        let issuer_id = match req.issuer_id {
            None => None,
            Some(id) => Some(
                id.parse::<IssuerId>()
                    .map_err(|_| Status::invalid_argument("invalid issuer id"))?,
            ),
        };

        let p = Policy::new(issuer_id, req.title, req.description, req.source)
            .map_err(|e| Status::invalid_argument(e.to_string()))?;

        let mut tx = self.db.tx().await;

        let mut policies = self.policies.write().await;
        policies.insert(p.id(), p.clone());

        self.db
            .insert_policy(&mut *tx, &p)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        res.policy = Some((&p).into());

        // NOTE: maybe we should not fail on client refresh
        self.refresh().await?;

        tx.commit()
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(res))
    }

    async fn read_policy(
        &self,
        req: tonic::Request<pb::ReadPolicyRequest>,
    ) -> std::result::Result<Response<pb::ReadPolicyResponse>, Status> {
        let mut res = pb::ReadPolicyResponse::default();

        let id = req
            .get_ref()
            .id
            .parse::<PolicyId>()
            .map_err(|e| Status::invalid_argument(e.to_string()))?;

        if let Some(p) = self.policies.read().await.get(&id) {
            res.policy = Some(p.into());
        } else {
            return Err(Status::not_found("no policy with specified id"));
        }

        Ok(Response::new(res))
    }

    async fn update_policy(
        &self,
        req: tonic::Request<pb::UpdatePolicyRequest>,
    ) -> std::result::Result<Response<pb::UpdatePolicyResponse>, Status> {
        let req = req.get_ref();
        let mut res = pb::UpdatePolicyResponse::default();

        let id = req
            .id
            .parse::<PolicyId>()
            .map_err(|e| Status::invalid_argument(e.to_string()))?;

        let mut policies = self.policies.write().await;

        let v = policies.get_mut(&id);
        if v.is_none() {
            return Err(Status::not_found("no policy with specified id"));
        }

        let mut tx = self.db.tx().await;

        let p = v.unwrap();
        if req.title.is_some() {
            p.set_title(req.title.clone());
        }
        if req.description.is_some() {
            p.set_description(req.description.clone());
        }
        if let Some(source) = req.statements.clone() {
            p.set_source(source)
                .map_err(|e| Status::invalid_argument(e.to_string()))?;
        }

        self.db
            .update_policy(&mut *tx, p)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        // NOTE: maybe we should not fail on client refresh
        self.refresh().await?;

        tx.commit()
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        res.policy = Some((&*p).into());

        Ok(Response::new(res))
    }

    async fn delete_policy(
        &self,
        req: tonic::Request<pb::DeletePolicyRequest>,
    ) -> std::result::Result<Response<()>, Status> {
        let id = &req
            .get_ref()
            .id
            .parse::<PolicyId>()
            .map_err(|e| Status::invalid_argument(e.to_string()))?;

        let mut tx = self.db.tx().await;

        let op = self
            .db
            .delete_policy(&mut *tx, id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        if op.rows_affected() == 0 {
            return Err(Status::not_found("no policy with specified id"));
        }

        self.policies.write().await.remove(id);

        // NOTE: maybe we should not fail on client refresh
        self.refresh().await?;

        tx.commit()
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(()))
    }

    async fn list_policies(
        &self,
        _: tonic::Request<pb::ListPoliciesRequest>,
    ) -> std::result::Result<Response<pb::ListPoliciesResponse>, Status> {
        let mut res = pb::ListPoliciesResponse::default();
        let policies = self.policies.read().await;
        res.policies = policies.values().map(Into::into).collect();
        Ok(Response::new(res))
    }

    async fn find_paths(
        &self,
        req: tonic::Request<pb::FindPathsRequest>,
    ) -> std::result::Result<Response<pb::FindPathsResponse>, Status> {
        let req = req.get_ref().clone();
        let mut res = pb::FindPathsResponse::default();

        let policies = self.policies.read().await.values().cloned().collect();
        let issuers = self.issuers.read().await.values().cloned().collect();
        let meta_policy = self.meta_policy.as_ref().map(|mp| mp.source().as_str());

        let nip_res = self
            .nip_proxy
            .clone() // FIXME: might be undesireable behavior
            .expect("nip proxy client not initialized")
            .get_metadata(nippb::GetMetadataRequest {
                src: req.src.clone(),
                dst: req.dst.clone(),
                topology: req
                    .links
                    .iter()
                    .map(|link| nippb::Link {
                        as_a: link.as_a.clone(),
                        if_a: link.if_a.clone(),
                        as_b: link.as_b.clone(),
                        if_b: link.if_b.clone(),
                    })
                    .collect(),
            })
            .await?;

        let pi = reasoner::ProblemInstance {
            src: req.src.to_owned(),
            dst: req.dst.to_owned(),
            links: req
                .links
                .iter()
                .map(|link| reasoner::Link {
                    as_a: link.as_a.to_owned(),
                    if_a: link.if_a.to_owned(),
                    as_b: link.as_b.to_owned(),
                    if_b: link.if_b.to_owned(),
                    meta: Some(
                        nip_res
                            .get_ref()
                            .link_info
                            .iter()
                            .filter(|info| {
                                info.link.as_ref().is_some_and(|info_link| {
                                    info_link.as_a == link.as_a
                                        && info_link.if_a == link.if_a
                                        && info_link.as_b == link.as_b
                                        && info_link.if_b == link.if_b
                                })
                            })
                            .map(|info| {
                                if info.value_bool.is_some() {
                                    reasoner::Metadata {
                                        name: info.name.to_owned(),
                                        value: reasoner::MetadataValue::Boolean(
                                            info.value_bool.unwrap(),
                                        ),
                                    }
                                } else if info.value_int32.is_some() {
                                    reasoner::Metadata {
                                        name: info.name.to_owned(),
                                        value: reasoner::MetadataValue::Numerical(
                                            info.value_int32.unwrap(),
                                        ),
                                    }
                                } else if info.value_string.is_some() {
                                    reasoner::Metadata {
                                        name: info.name.to_owned(),
                                        value: reasoner::MetadataValue::Categorical(
                                            info.value_string.to_owned().unwrap(),
                                        ),
                                    }
                                } else {
                                    panic!("nip proxy is returning invalid data")
                                }
                            })
                            .collect(),
                    ),
                })
                .collect(),
            meta: nip_res
                .get_ref()
                .node_info
                .iter()
                .map(|info| {
                    if info.value_bool.is_some() {
                        reasoner::GlobalMetadata {
                            name: info.name.to_owned(),
                            subj: Some(info.node.to_owned()),
                            value: reasoner::MetadataValue::Boolean(info.value_bool.unwrap()),
                        }
                    } else if info.value_int32.is_some() {
                        reasoner::GlobalMetadata {
                            name: info.name.to_owned(),
                            subj: Some(info.node.to_owned()),
                            value: reasoner::MetadataValue::Numerical(info.value_int32.unwrap()),
                        }
                    } else if info.value_string.is_some() {
                        reasoner::GlobalMetadata {
                            name: info.name.to_owned(),
                            subj: Some(info.node.to_owned()),
                            value: reasoner::MetadataValue::Categorical(
                                info.value_string.to_owned().unwrap(),
                            ),
                        }
                    } else {
                        panic!("nip proxy is returning invalid data")
                    }
                })
                .collect(),
        };

        let solution =
            reasoner::solve(&pi, policies, issuers, meta_policy).map_err(|err| match err {
                ReasonerError::AspError(e) => Status::internal(e.to_string()),
                ReasonerError::ConflictResolutionError(e) => Status::aborted(e.to_string()),
                ReasonerError::InvalidMetaInstance => {
                    Status::aborted("invalid meta-policy instance".to_string())
                }
            })?;

        if let Some(paths) = solution {
            res.paths = paths
                .iter()
                .map(|p| pb::Path {
                    links: p
                        .iter()
                        .map(|link| pb::Link {
                            as_a: link.as_a.to_owned(),
                            if_a: link.if_a.to_owned(),
                            as_b: link.as_b.to_owned(),
                            if_b: link.if_b.to_owned(),
                        })
                        .collect(),
                })
                .collect();
        }

        Ok(Response::new(res))
    }

    async fn register_issuer(
        &self,
        request: tonic::Request<pb::RegisterIssuerRequest>,
    ) -> std::result::Result<Response<pb::RegisterIssuerResponse>, Status> {
        let req = request.get_ref().clone();
        let mut res = pb::RegisterIssuerResponse::default();

        let issuer = Issuer::new(req.name, req.rank, req.description);

        let mut tx = self.db.tx().await;

        let mut issuers = self.issuers.write().await;
        issuers.insert(issuer.id(), issuer.clone());

        self.db
            .insert_issuer(&mut *tx, &issuer)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        res.issuer = Some((&issuer).into());

        // NOTE: maybe we should not fail on client refresh
        self.refresh().await?;

        tx.commit()
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(res))
    }

    async fn subscribe_path_analyzer(&self, request: Request<()>) -> Result<Response<()>, Status> {
        let addr = request.remote_addr().ok_or(Status::internal(
            "could not extract remote address from request",
        ))?;

        let chan = PathAnalyzerClient::connect(addr.to_string())
            .await
            .map_err(|e| Status::unknown(e.to_string()))?;

        // NOTE: maybe we should not refresh on new client registration
        let mut clients = CLIENTS.lock().await;
        let mut client = ClientHandle {
            addr,
            chan,
            stale: true,
        };
        client.refresh().await?;
        clients.push(client);

        Ok(Response::new(()))
    }
}
