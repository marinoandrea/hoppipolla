import winston from "winston";

const format = winston.format.printf(({ level, message }) => {
  return `${new Date().toISOString()} [${level}]: ${message}`;
});

const logger = winston
  .createLogger({
    level: process.env.LOG_LEVEL,
    format,
  })
  .add(
    process.env.NODE_ENV === "production"
      ? new winston.transports.Stream({ format, stream: process.stdout })
      : new winston.transports.Console({ format })
  );

export default logger;
