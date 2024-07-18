import {
  DataReading,
  IsdAs,
  ReadingCollectionQuery,
} from "src/domain/entities";
import { IReadingSource } from "src/domain/repositories";

export class InMemoryReadingSource<TReading extends DataReading>
  implements IReadingSource<TReading>
{
  private identityMap: Map<IsdAs, TReading[]>;

  constructor(identityMap: Map<IsdAs, TReading[]> = new Map()) {
    this.identityMap = identityMap;
  }

  async fetchAllInInterval(query: ReadingCollectionQuery): Promise<TReading[]> {
    if (!this.identityMap.has(query.isdAs)) {
      this.identityMap.set(query.isdAs, []);
      return Promise.resolve([]);
    }

    const filteredData = this.identityMap
      .get(query.isdAs)!
      .filter(
        (reading) =>
          reading.collectedAt >= query.startTime &&
          reading.collectedAt <= query.endTime
      );

    return Promise.resolve(filteredData);
  }
}
