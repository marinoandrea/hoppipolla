import { createClient } from "redis";

import { Repository } from "redis-om";
import logger from "src/logging";
import { energyReadingSchema } from "./schema";

export const redisClient = createClient();

export type RedisClient = typeof redisClient;

export async function initRedisClient() {
  redisClient.on("error", logger.error);

  await redisClient.connect();

  const energyReadingRepository = new Repository(
    energyReadingSchema,
    redisClient
  );

  await energyReadingRepository.createIndex();
}
