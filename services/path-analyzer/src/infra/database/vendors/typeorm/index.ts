import "reflect-metadata";
import { DataSource } from "typeorm";

import { config } from "src/config";

import { HopModel, NodeModel, PathModel } from "./models";

export const AppDataSource = new DataSource({
  type: "better-sqlite3",
  database: config.SQLITE_URI,
  synchronize: true,
  logging: config.NODE_ENV === "development",
  entities: [PathModel, NodeModel, HopModel],
  subscribers: [],
  migrations: [],
});
