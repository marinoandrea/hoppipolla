import { createClient } from "redis";

import { Repository } from "redis-om";
import { energyReadingSchema } from "./schema";

export const redisClient = createClient();

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
