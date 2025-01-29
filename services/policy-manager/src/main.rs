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

#[derive(Envconfig, Debug, Default, Clone)]
struct Config {
    #[envconfig(from = "DB_URI")]
    pub db_uri: String,

    #[envconfig(from = "DB_MAX_CONNECTIONS", default = "20")]
    pub db_max_conns: u32,

    #[envconfig(from = "PORT", default = "27002")]
    pub port: u16,

    #[envconfig(from = "NIP_PROXY_ADDR", default = "127.0.0.1:27003")]
    pub nip_proxy_addr: String,
}

#[tokio::main]
async fn main() {
    env_logger::builder()
        .target(env_logger::Target::Stdout)
        .init();

    log::set_max_level(log::LevelFilter::Info);

    println!("Started");

    let config = Config::init_from_env().expect("could not extract config from env");
    let addr = format!("0.0.0.0:{}", config.port)
        .parse()
        .expect("failed to parse address");

    let mut app = Service::with_config(config.clone()).await;
    app.init().await.expect("failed to init service");

    println!("Initialized service listening on port {}", config.port);

    let daemon_handle = tokio::spawn(run_broadcast_daemon());

    let status = tonic::transport::Server::builder()
        .add_service(pb::PolicyManagerServer::new(app))
        .serve(addr)
        .await;

    if status.is_err() {
        let err = status.err().unwrap();
        println!("ERROR: {}", err);
    }

    let _ = daemon_handle
        .await
        .expect("failed to close broadcaster daemon thread");
}
