import { DataReading, IsdAs } from "src/domain/entities";
import {
  IReadingCollectionRepository,
  ReadingCollectionQuery,
} from "src/domain/repositories";

export class InMemoryReadingCollectionRepository<TReading extends DataReading>
  implements IReadingCollectionRepository<TReading>
{
  private identityMap: Map<IsdAs, TReading[]>;

  constructor(identityMap: Map<IsdAs, TReading[]> = new Map()) {
    this.identityMap = identityMap;
  }

  getAllInInterval(query: ReadingCollectionQuery): Promise<TReading[]> {
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

  store(isdAs: IsdAs, ...entities: TReading[]): Promise<void> {
    if (!this.identityMap.has(isdAs)) {
      this.identityMap.set(isdAs, []);
    }
    this.identityMap.get(isdAs)!.push(...entities);
    return Promise.resolve();
  }
}
