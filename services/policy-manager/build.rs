fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::configure()
        .protoc_arg("--experimental_allow_proto3_optional")
        .compile_protos(
            &[
                "../../proto/policy_manager/v1/service.proto",
                "../../proto/path_analyzer/v1/service.proto",
                "../../proto/nip_proxy/v1/service.proto",
            ],
            &["../../proto"],
        )?;
    Ok(())
}
