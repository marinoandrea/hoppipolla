import { z } from "zod";

export const config = z
  .object({
    NODE_ENV: z
      .enum(["development", "test", "staging", "production"])
      .default("development"),
    HOST: z.string().default("127.0.0.1"),
    PORT: z.coerce.number().default(27_004),
    SCIOND_URI: z.string().default("127.0.0.1:30255"),
    SCION_EXE_PATH: z.string().default("scion"),
    PATH_ANALYZER_URI: z.string().default("127.0.0.1:27001"),
    POLICY_MANAGER_URI: z.string().default("127.0.0.1:27002"),
    NIP_PROXY_URI: z.string().default("127.0.0.1:27003"),
    LOG_LEVEL: z
      .enum(["info", "error", "debug", "warning", "silly"])
      .default("debug"),
  })
  .parse(process.env);
