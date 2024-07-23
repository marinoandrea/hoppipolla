import { Repository, Schema } from "redis-om";

import {
  DataReading,
  EnergyReading,
  GeoReading,
  IsdAs,
  ReadingCollectionQuery,
  validateEnergyReading,
  validateGeoReading,
} from "src/domain/entities";
import { IReadingCollectionRepository } from "src/domain/repositories";

import { RedisClient } from ".";
import { energyReadingSchema, geoReadingSchema } from "./schema";

abstract class RedisReadingCollectionRepository<TReading extends DataReading>
  implements IReadingCollectionRepository<TReading>
{
  private repository: Repository<TReading>;

  constructor(client: RedisClient, schema: Schema<TReading>) {
    this.repository = new Repository(schema, client);
  }

  // NOTE: redis-om does not do type inference, therefore we cannot take full
  // advantage of this pattern. This implementation might need to change.
  abstract mapHashToReading(hash: Record<string, unknown>): TReading;

  async getAllInInterval(query: ReadingCollectionQuery): Promise<TReading[]> {
    const hashes = await this.repository
      .search()
      // @ts-expect-error redis-om does not do type inference
      .where("collectedAt")
      .greaterThanOrEqualTo(query.startTime)
      // @ts-expect-error redis-om does not do type inference
      .and("collectedAt")
      .lessThanOrEqualTo(query.endTime)
      // @ts-expect-error redis-om does not do type inference
      .and("isdAs")
      .equal(query.isdAs)
      .returnAll();
    // NOTE: this enforces data structure contract internally but might slow
    // down retrieval excessively
    return hashes.map(this.mapHashToReading);
  }

  async store(isdAs: IsdAs, ...entities: TReading[]): Promise<void> {
    await Promise.all(
      entities.map((entity) => this.repository.save({ ...entity, isdAs }))
    );
  }
}

export class RedisEnergyReadingRepository extends RedisReadingCollectionRepository<EnergyReading> {
  constructor(client: RedisClient) {
    super(client, energyReadingSchema);
  }

  mapHashToReading(hash: Record<string, unknown>) {
    return validateEnergyReading(hash);
  }
}

export class RedisGeoReadingRepository extends RedisReadingCollectionRepository<GeoReading> {
  constructor(client: RedisClient) {
    super(client, geoReadingSchema);
  }

  mapHashToReading(hash: Record<string, unknown>) {
    return validateGeoReading(hash);
  }
}
