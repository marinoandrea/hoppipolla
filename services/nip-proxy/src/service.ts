import { config } from "./config";
import { ReadingCollectionQuery } from "./domain/entities";
import { queryAndUpdateRepository } from "./domain/use-cases";
import { redisClient } from "./infra/repositories/redis";
import { RedisEnergyReadingRepository } from "./infra/repositories/redis/repositories";
import { FilesystemMockEnergyReadingSource } from "./infra/sources/filesystem-mock";

export class NipProxyService {
  public static async executeGetAsEnergyData(query: ReadingCollectionQuery) {
    const energyReadingRepository = new RedisEnergyReadingRepository(
      redisClient
    );
    const energyReadingSource = new FilesystemMockEnergyReadingSource(
      config.ENERGY_READING_MOCKFILE
    );
    return await queryAndUpdateRepository(
      energyReadingRepository,
      energyReadingSource,
      query
    );
  }
}
