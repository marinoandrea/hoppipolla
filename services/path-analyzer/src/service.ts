import { config } from "./config";
import { getPathForAddress } from "./domain/use-cases";
import { AppDataSource } from "./infra/database/vendors/typeorm";
import {
  TypeOrmNodeRepository,
  TypeOrmPathRepository,
} from "./infra/database/vendors/typeorm/repositories";
import { PolicyManagerGrpcClient } from "./infra/services/policy-manager/vendors/grpc";
import { ScionSubprocessClient } from "./infra/services/scion-client/vendors/subprocess";
import logger from "./logging";

export class PathAnalyzerService {
  public static async executeGetPathForAddress(address: string) {
    const session = AppDataSource.createQueryRunner();
    await session.startTransaction();

    try {
      const pathRepository = new TypeOrmPathRepository(session);
      const nodeRepository = new TypeOrmNodeRepository(session);
      const policyManager = new PolicyManagerGrpcClient(
        config.POLICY_MANAGER_URI
      );
      const scionClient = new ScionSubprocessClient(config.SCIOND_URI);

      const output = await getPathForAddress(
        pathRepository,
        nodeRepository,
        policyManager,
        scionClient,
        address
      );

      await session.commitTransaction();

      return output;
    } catch (e) {
      logger.error(e);
      await session.rollbackTransaction();
      throw e;
    }
  }
}
