import { createClient } from "redis";

import { Repository } from "redis-om";
import { config } from "src/config";
import { energyReadingSchema } from "./schema";

export const redisClient = createClient({ url: config.REDIS_URI });

export type RedisClient = typeof redisClient;

export async function initRedisClient() {
  redisClient.on("error", console.error);

  await redisClient.connect();

  const energyReadingRepository = new Repository(
    energyReadingSchema,
    redisClient
  );

  await energyReadingRepository.createIndex();
}
