import "reflect-metadata";
import { DataSource } from "typeorm";

import { config } from "src/config";

import { HopModel, NodeModel, PathModel } from "./models";

export const AppDataSource = new DataSource({
  type: "better-sqlite3",
  database: config.DATABASE_URI,
  synchronize: config.NODE_ENV === "development",
  logging: config.LOG_LEVEL === "silly",
  entities: [PathModel, NodeModel, HopModel],
  subscribers: [],
  migrations: [],
});
