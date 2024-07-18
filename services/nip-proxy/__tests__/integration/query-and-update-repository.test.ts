import { expect, test } from "@jest/globals";

import { EnergyReading, IsdAs } from "src/domain/entities";
import { EntityValidationError } from "src/domain/errors";
import { queryAndUpdateRepository } from "src/domain/use-cases";
import { InMemoryReadingCollectionRepository } from "src/infra/repositories/in-memory";
import { InMemoryReadingSource } from "src/infra/sources/in-memory";

const isdAs = "1-ff00:0:110";

test("throws an error when the ISD-AS specifier is malformed", async () => {
  const energyReadingRepository =
    new InMemoryReadingCollectionRepository<EnergyReading>();
  const energyReadingSource = new InMemoryReadingSource<EnergyReading>();

  try {
    await queryAndUpdateRepository(
      energyReadingRepository,
      energyReadingSource,
      {
        isdAs: "malformed-id",
        startTime: new Date(),
        endTime: new Date(),
      }
    );
  } catch (e) {
    expect(e).toBeInstanceOf(EntityValidationError);
    const eSpecific = e as EntityValidationError;
    expect(eSpecific.field).toBe("isdAs");
  }
});

test("throws an error when the startTime is invalid", async () => {
  const energyReadingRepository =
    new InMemoryReadingCollectionRepository<EnergyReading>();
  const energyReadingSource = new InMemoryReadingSource<EnergyReading>();

  try {
    await queryAndUpdateRepository(
      energyReadingRepository,
      energyReadingSource,
      {
        isdAs,
        // NOTE: boundary value analysis cannot be done due to potential
        // gap between time of input and time of validation, 100ms seems fine to
        // test this functionality
        startTime: new Date(new Date().getTime() + 100),
        endTime: new Date(),
      }
    );
  } catch (e) {
    expect(e).toBeInstanceOf(EntityValidationError);
    const eSpecific = e as EntityValidationError;
    expect(eSpecific.field).toBe("startTime");
  }
});

test("throws an error when the endTime is invalid", async () => {
  const energyReadingRepository =
    new InMemoryReadingCollectionRepository<EnergyReading>();
  const energyReadingSource = new InMemoryReadingSource<EnergyReading>();

  try {
    await queryAndUpdateRepository(
      energyReadingRepository,
      energyReadingSource,
      {
        isdAs,
        startTime: new Date(),
        // NOTE: boundary value analysis cannot be done due to potential
        // gap between time of input and time of validation, 100ms seems fine to
        // test this functionality
        endTime: new Date(new Date().getTime() + 100),
      }
    );
  } catch (e) {
    expect(e).toBeInstanceOf(EntityValidationError);
    const eSpecific = e as EntityValidationError;
    expect(eSpecific.field).toBe("endTime");
  }
});

test("returns an empty list when there is no entry for the AS", async () => {
  const energyReadingRepository =
    new InMemoryReadingCollectionRepository<EnergyReading>();
  const energyReadingSource = new InMemoryReadingSource<EnergyReading>();

  const output = await queryAndUpdateRepository(
    energyReadingRepository,
    energyReadingSource,
    {
      isdAs,
      startTime: new Date(),
      endTime: new Date(),
    }
  );

  expect(output).toHaveLength(0);
});

test("returns readings between startTime and endTime when all the readings are already cached", async () => {
  const now = new Date();

  const energyReadingRepository =
    new InMemoryReadingCollectionRepository<EnergyReading>(
      new Map<IsdAs, EnergyReading[]>([
        [
          isdAs,
          [
            {
              id: "reading-1",
              isdAs,
              collectedAt: now,
              machineId: "machine-1",
            },
            {
              id: "reading-2",
              isdAs,
              collectedAt: now,
              machineId: "machine-2",
            },
          ],
        ],
      ])
    );

  const energyReadingSource = new InMemoryReadingSource<EnergyReading>();

  const output = await queryAndUpdateRepository(
    energyReadingRepository,
    energyReadingSource,
    {
      isdAs,
      startTime: now,
      endTime: now,
    }
  );

  expect(output).toHaveLength(2);
});

test("returns all readings when those after startTime + X are already cached", async () => {
  const now = new Date();

  const startTime = new Date(now.getTime() - 100);
  const endTime = now;

  const energyReadingRepository =
    new InMemoryReadingCollectionRepository<EnergyReading>(
      new Map<IsdAs, EnergyReading[]>([
        [
          isdAs,
          [
            {
              id: "reading-1",
              isdAs,
              collectedAt: endTime,
              machineId: "machine-1",
            },
            {
              id: "reading-2",
              isdAs,
              collectedAt: endTime,
              machineId: "machine-2",
            },
          ],
        ],
      ])
    );

  const energyReadingSource = new InMemoryReadingSource<EnergyReading>(
    new Map<IsdAs, EnergyReading[]>([
      [
        isdAs,
        [
          {
            id: "reading-1",
            isdAs,
            collectedAt: startTime,
            machineId: "machine-1",
          },
          {
            id: "reading-2",
            isdAs,
            collectedAt: startTime,
            machineId: "machine-2",
          },
        ],
      ],
    ])
  );

  const output = await queryAndUpdateRepository(
    energyReadingRepository,
    energyReadingSource,
    {
      isdAs,
      startTime,
      endTime,
    }
  );

  expect(output).toHaveLength(4);
});

test("returns all readings when those before endTime - X are already cached", async () => {
  const now = new Date();

  const startTime = new Date(now.getTime() - 100);
  const endTime = now;

  const energyReadingRepository =
    new InMemoryReadingCollectionRepository<EnergyReading>(
      new Map<IsdAs, EnergyReading[]>([
        [
          isdAs,
          [
            {
              id: "reading-1",
              isdAs,
              collectedAt: startTime,
              machineId: "machine-1",
            },
            {
              id: "reading-2",
              isdAs,
              collectedAt: startTime,
              machineId: "machine-2",
            },
          ],
        ],
      ])
    );

  const energyReadingSource = new InMemoryReadingSource<EnergyReading>(
    new Map<IsdAs, EnergyReading[]>([
      [
        isdAs,
        [
          {
            id: "reading-1",
            isdAs,
            collectedAt: endTime,
            machineId: "machine-1",
          },
          {
            id: "reading-2",
            isdAs,
            collectedAt: endTime,
            machineId: "machine-2",
          },
        ],
      ],
    ])
  );

  const output = await queryAndUpdateRepository(
    energyReadingRepository,
    energyReadingSource,
    {
      isdAs,
      startTime,
      endTime,
    }
  );

  expect(output).toHaveLength(4);
});

test("returns all readings when those before endTime - X and after starTime + 100 are already cached", async () => {
  const now = new Date();

  const queryStartTime = new Date(now.getTime() - 300);
  const queryEndTime = now;
  const storedStartTime = new Date(now.getTime() - 200);
  const storedEndTime = new Date(now.getTime() - 100);

  const energyReadingRepository =
    new InMemoryReadingCollectionRepository<EnergyReading>(
      new Map<IsdAs, EnergyReading[]>([
        [
          isdAs,
          [
            {
              id: "reading-1",
              isdAs,
              collectedAt: storedStartTime,
              machineId: "machine-1",
            },
            {
              id: "reading-2",
              isdAs,
              collectedAt: storedStartTime,
              machineId: "machine-2",
            },
            {
              id: "reading-3",
              isdAs,
              collectedAt: storedEndTime,
              machineId: "machine-1",
            },
            {
              id: "reading-4",
              isdAs,
              collectedAt: storedEndTime,
              machineId: "machine-2",
            },
          ],
        ],
      ])
    );

  const energyReadingSource = new InMemoryReadingSource<EnergyReading>(
    new Map<IsdAs, EnergyReading[]>([
      [
        isdAs,
        [
          {
            id: "reading-1",
            isdAs,
            collectedAt: queryStartTime,
            machineId: "machine-1",
          },
          {
            id: "reading-2",
            isdAs,
            collectedAt: queryStartTime,
            machineId: "machine-2",
          },
          {
            id: "reading-1",
            isdAs,
            collectedAt: queryEndTime,
            machineId: "machine-1",
          },
          {
            id: "reading-2",
            isdAs,
            collectedAt: queryEndTime,
            machineId: "machine-2",
          },
        ],
      ],
    ])
  );

  const output = await queryAndUpdateRepository(
    energyReadingRepository,
    energyReadingSource,
    {
      isdAs,
      startTime: queryStartTime,
      endTime: queryEndTime,
    }
  );

  expect(output).toHaveLength(8);
});
