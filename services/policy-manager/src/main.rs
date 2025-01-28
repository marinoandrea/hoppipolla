use envconfig::Envconfig;

pub mod policy_manager {
    tonic::include_proto!("proto.hoppipolla.policy_manager.v1");
}

pub mod path_analyzer {
    tonic::include_proto!("proto.hoppipolla.path_analyzer.v1");
}

pub mod nip_proxy {
    tonic::include_proto!("proto.hoppipolla.nip_proxy.v1");
}

mod db;
mod entities;
mod reasoner;
mod service;

use policy_manager::policy_manager_server as pb;
use service::{run_broadcast_daemon, Service};

#[derive(Envconfig, Debug, Default)]
struct Config {
    #[envconfig(from = "DB_URI")]
    pub db_uri: String,

    #[envconfig(from = "DB_MAX_CONNECTIONS", default = "20")]
    pub db_max_conns: u32,

    #[envconfig(from = "PORT", default = "27001")]
    pub port: u16,

    #[envconfig(from = "NIP_PROXY_ADDR", default = "127.0.0.1:27003")]
    pub nip_proxy_addr: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    env_logger::init();

    let config = Config::init_from_env().expect("could not extract config from env");
    let addr = format!("[::1]:{}", config.port).parse()?;

    let mut app = Service::with_config(config).await;
    app.init().await.expect("failed to init service");

    tokio::try_join!(
        run_broadcast_daemon(),
        tonic::transport::Server::builder()
            .add_service(pb::PolicyManagerServer::new(app))
            .serve(addr)
    )?;

    Ok(())
}
