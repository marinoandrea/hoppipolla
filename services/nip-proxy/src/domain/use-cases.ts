import { DataReading } from "./entities";
import {
  IReadingCollectionRepository,
  IReadingSource,
  ReadingCollectionQuery,
} from "./repositories";

export async function queryAndUpdateRepository<TReading extends DataReading>(
  readingRepository: IReadingCollectionRepository<TReading>,
  readingSource: IReadingSource<TReading>,
  query: ReadingCollectionQuery
) {
  const storedEntities = await readingRepository.getAllInInterval(query);

  // find gaps in the requested data
  let minStoredCollectedAt = new Date();
  let maxStoredCollectedAt = new Date(0);
  for (const entity of storedEntities) {
    minStoredCollectedAt =
      entity.collectedAt < minStoredCollectedAt
        ? entity.collectedAt
        : minStoredCollectedAt;
    maxStoredCollectedAt =
      entity.collectedAt > maxStoredCollectedAt
        ? entity.collectedAt
        : maxStoredCollectedAt;
  }

  // conditionally request more data from source in the missing intervals
  const tasks = [];

  if (minStoredCollectedAt > query.startTime) {
    tasks.push(
      readingSource.fetchAllInInterval({
        ...query,
        endTime: minStoredCollectedAt,
      })
    );
  }

  if (maxStoredCollectedAt < query.endTime) {
    tasks.push(
      readingSource.fetchAllInInterval({
        ...query,
        startTime: maxStoredCollectedAt,
      })
    );
  }

  const [beforeEntities, afterEntities] = await Promise.all(tasks);

  // defer the storage operation to speed up the service response
  using cleanup = new DisposableStack();

  cleanup.defer(async () => {
    await readingRepository.store(
      query.isdAs,
      ...beforeEntities,
      ...afterEntities
    );
  });

  return [...beforeEntities, ...storedEntities, ...afterEntities];
}
