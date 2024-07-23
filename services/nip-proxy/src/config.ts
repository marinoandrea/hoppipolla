import { z } from "zod";

export const config = z
  .object({
    NODE_ENV: z
      .enum(["development", "test", "staging", "production"])
      .default("development"),
    HOST: z.string().default("127.0.0.1"),
    PORT: z.coerce.number().default(27_003),
    LOG_LEVEL: z.enum(["info", "error", "debug", "warning"]).default("debug"),
    REDIS_URI: z.string().default("redis://127.0.0.1:6379"),
    ENERGY_READING_MOCKFILE: z.string().default("mocks/energy.json"),
    GEO_READING_MOCKFILE: z.string().default("mocks/geography.json"),
  })
  .parse(process.env);
