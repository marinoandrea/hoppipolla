const before = new Date().getTime();

import { config } from "./config";

import * as grpc from "@grpc/grpc-js";

import { NipProxyGrpcService } from "./grpc";
import { initRedisClient } from "./infra/repositories/redis";
import logger from "./logging";
import { hoppipolla as pb } from "./protos/nip";

async function main() {
  const server = new grpc.Server();

  server.addService(
    pb.nip.UnimplementedNipProxyService.definition,
    new NipProxyGrpcService()
  );

  try {
    await initRedisClient();
  } catch (e) {
    console.error(e);
    return;
  }

  const address = `${config.HOST}:${config.PORT}`;

  server.bindAsync(
    address,
    grpc.ServerCredentials.createInsecure(),
    (err, port) => {
      if (err != null) {
        logger.error(err);
        return;
      }

      const after = new Date().getTime();
      logger.info(`service | running`);
      logger.info(`node    | ${process.version}`);
      logger.info(`env     | ${config.NODE_ENV}`);
      logger.info(`address | ${config.HOST}:${port}`);
      logger.info(`startup | ${after - before}ms`);
    }
  );
}

main();
