import { DataReading, IsdAs } from "./entities";

export type ReadingCollectionQuery = {
  isdAs: IsdAs;
  startTime: Date;
  endTime: Date;
};

/**
 * Interface for an implementation of the repository pattern for a
 * specific collection of entities.
 *
 * This service specializes in retrieving and serving large collections of data,
 * grouped by ids of network nodes. Therefore, a traditional entity-by-entity
 * approach is less effective.
 */
export interface IReadingCollectionRepository<TReading extends DataReading> {
  /**
   * Retrieve all entities associated with the specified identifier in the
   * provided interval of time. This filters the returned entity by their
   * `collectedAt` field.
   *
   * @param id The unique identifier for entity groups
   */
  getAllInInterval(query: ReadingCollectionQuery): Promise<TReading[]>;

  store(id: IsdAs, ...entities: TReading[]): Promise<void>;
}

export interface IReadingSource<TReading extends DataReading> {
  fetchAllInInterval(query: ReadingCollectionQuery): Promise<TReading[]>;
}
