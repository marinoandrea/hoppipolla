fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::compile_protos("../../proto/policy_manager/v1/service.proto")?;
    tonic_build::compile_protos("../../proto/path_analyzer/v1/service.proto")?;
    tonic_build::compile_protos("../../proto/nip_proxy/v1/service.proto")?;
    Ok(())
}
