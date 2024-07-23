import { config } from "./config";
import { ReadingCollectionQuery } from "./domain/entities";
import { queryAndUpdateRepository } from "./domain/use-cases";
import { redisClient } from "./infra/repositories/redis";
import {
  RedisEnergyReadingRepository,
  RedisGeoReadingRepository,
} from "./infra/repositories/redis/repositories";
import {
  FilesystemMockEnergyReadingSource,
  FilesystemMockGeoReadingSource,
} from "./infra/sources/filesystem-mock";

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

  public static async executeGetAsGeoData(query: ReadingCollectionQuery) {
    const geoReadingRepository = new RedisGeoReadingRepository(redisClient);
    const geoReadingSource = new FilesystemMockGeoReadingSource(
      config.GEO_READING_MOCKFILE
    );
    return await queryAndUpdateRepository(
      geoReadingRepository,
      geoReadingSource,
      query
    );
  }
}
