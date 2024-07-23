import { PathLike } from "fs";
import { readFile } from "fs/promises";
import { z } from "zod";

import {
  DataReading,
  EnergyReading,
  energyReadingSchema,
  GeoReading,
  geoReadingSchema,
  isdAsSchema,
  ReadingCollectionQuery,
} from "src/domain/entities";
import { IReadingSource } from "src/domain/repositories";

abstract class FilesystemMockReadingSource<TReading extends DataReading>
  implements IReadingSource<TReading>
{
  private path: PathLike;
  private schema: z.ZodRecord<z.ZodString, z.ZodArray<z.ZodSchema<TReading>>>;

  constructor(path: PathLike, schema: z.ZodSchema<TReading>) {
    this.path = path;
    this.schema = z.record(isdAsSchema, z.array(schema));
  }

  async fetchAllInInterval(query: ReadingCollectionQuery): Promise<TReading[]> {
    const raw = await readFile(this.path, { encoding: "utf8" });
    const json = JSON.parse(raw);
    const validated = await this.schema.parseAsync(json);
    return validated[query.isdAs].filter(
      (reading) =>
        reading.collectedAt >= query.startTime &&
        reading.collectedAt <= query.endTime
    );
  }
}

export class FilesystemMockEnergyReadingSource extends FilesystemMockReadingSource<EnergyReading> {
  constructor(path: PathLike) {
    super(path, energyReadingSchema);
  }
}

export class FilesystemMockGeoReadingSource extends FilesystemMockReadingSource<GeoReading> {
  constructor(path: PathLike) {
    super(path, geoReadingSchema);
  }
}
