import { DataReading, validateReadingCollectionQuery } from "./entities";
import { IReadingCollectionRepository, IReadingSource } from "./repositories";

type QueryAndUpdateRepositoryInput = {
  isdAs: string;
  startTime: Date;
  endTime: Date;
};

export async function queryAndUpdateRepository<TReading extends DataReading>(
  readingRepository: IReadingCollectionRepository<TReading>,
  readingSource: IReadingSource<TReading>,
  query: QueryAndUpdateRepositoryInput
) {
  const validatedQuery = validateReadingCollectionQuery(query);

  const storedEntities =
    await readingRepository.getAllInInterval(validatedQuery);

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

  const results = await Promise.all(tasks);
  const fetchedEntities = results.flat();

  // defer the storage operation to speed up the service response
  try {
    return [...fetchedEntities, ...storedEntities];
  } finally {
    await readingRepository.store(query.isdAs, ...fetchedEntities);
    /*
    FIXME: this is the right way to do it, however DisposableStack appears
    to be not defined even when including lib.esnext.disposable

    using cleanup = new DisposableStack();

    cleanup.defer(async () => {
      await readingRepository.store(
        query.isdAs,
        ...beforeEntities,
        ...afterEntities
      );
    })
    */
  }
}
