import { z } from "zod";

const hostSchema = z.string().regex(/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/);

export const config = z
  .object({
    NODE_ENV: z
      .enum(["development", "test", "staging", "production"])
      .default("development"),
    HOST: hostSchema.optional().default("0.0.0.0"),
    PORT: z.coerce.number().default(27_001),
    MAX_PATHS_BATCH: z.coerce.number().int().gt(0).default(10),
    SCIOND_URI: z.string().default("127.0.0.1:30255"),
    SQLITE_URI: z.string().default("file://sqlite.db"),
    POLICY_MANAGER_URI: z.string().default("localhost:27002"),
  })
  .parse(process.env);
