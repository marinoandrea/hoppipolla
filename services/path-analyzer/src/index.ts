const before = new Date().getTime();

import { config } from "./config";

import * as grpc from "@grpc/grpc-js";

import { PathAnalyzerGrpcService } from "./grpc";
import logger from "./logging";
import { hoppipolla } from "./protos/path";

async function main() {
  const server = new grpc.Server();

  server.addService(
    hoppipolla.path.UnimplementedPathAnalyzerService.definition,
    new PathAnalyzerGrpcService()
  );

  server.bindAsync(
    `${config.HOST}:${config.PORT}`,
    grpc.ServerCredentials.createInsecure(),
    (err) => {
      if (err != null) {
        return console.error(err);
      }

      const after = new Date().getTime();
      logger.info(`service | running`);
      logger.info(`node    | ${process.version}`);
      logger.info(`env     | ${config.NODE_ENV}`);
      logger.info(`address | ${config.HOST}:${config.PORT}`);
      logger.info(`startup | ${after - before}ms`);
    }
  );
}

main();
