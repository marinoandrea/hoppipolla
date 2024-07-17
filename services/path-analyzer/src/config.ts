import { z } from "zod";

export const config = z
  .object({
    NODE_ENV: z
      .enum(["development", "test", "staging", "production"])
      .default("development"),
    HOST: z.string().default("127.0.0.1"),
    PORT: z.coerce.number().default(27_001),
    SCIOND_URI: z.string().default("127.0.0.1:30255"),
    DATABASE_URI: z.string().default("file://sqlite.db"),
    POLICY_MANAGER_URI: z.string().default("localhost:27002"),
    MAX_PATHS_BATCH: z.coerce.number().int().gt(0).default(10),
  })
  .parse(process.env);
