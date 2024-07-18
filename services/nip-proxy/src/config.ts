import { z } from "zod";

export const config = z
  .object({
    NODE_ENV: z
      .enum(["development", "test", "staging", "production"])
      .default("development"),
    HOST: z.string().default("127.0.0.1"),
    PORT: z.coerce.number().default(27_001),
    LOG_LEVEL: z.enum(["info", "error", "debug", "warning"]).default("debug"),
    ENERGY_READING_MOCKFILE: z.string().default("mocks/energy-readings.json"),
  })
  .parse(process.env);
