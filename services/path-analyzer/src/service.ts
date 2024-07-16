import { config } from "./config";
import { getPathForAddress } from "./domain/use-cases";
import { AppDataSource } from "./infra/database/vendors/typeorm";
import {
  TypeOrmNodeRepository,
  TypeOrmPathRepository,
} from "./infra/database/vendors/typeorm/repositories";
import { PolicyManagerGrpcClient } from "./infra/services/policy-manager/vendors/grpc";
import { ScionSubprocessClient } from "./infra/services/scion-client/vendors/subprocess";

export class PathAnalyzerService {
  public static async executeGetPathForAddress(address: string) {
    const session = AppDataSource.createQueryRunner();
    const pathRepository = new TypeOrmPathRepository(session);
    const nodeRepository = new TypeOrmNodeRepository(session);
    const policyManager = new PolicyManagerGrpcClient(
      config.POLICY_MANAGER_URI
    );
    const scionClient = new ScionSubprocessClient(config.SCIOND_URI);
    return await getPathForAddress(
      pathRepository,
      nodeRepository,
      policyManager,
      scionClient,
      address
    );
  }
}
