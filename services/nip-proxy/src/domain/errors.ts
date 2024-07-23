import { z } from "zod";

export class EntityValidationError extends Error {
  public static code = 400;

  public entity: string;
  public field: string;
  public message: string;

  constructor(entity: string, field: string, message: string) {
    super(`[${entity}] ${field}: ${message}`);
    this.entity = entity;
    this.field = field;
    this.message = message;
  }
}

export class InternalError extends Error {
  public static code = 500;
}

export function handleZodValidation<T>(
  entity: string,
  parse: (data: unknown) => T
) {
  return (data: unknown) => {
    try {
      return parse(data);
    } catch (e) {
      if (!(e instanceof z.ZodError)) {
        throw e;
      }

      const issue = e.issues.pop();
      if (!issue) {
        throw new InternalError(`Validation failed for unknown reasons: ${e}`);
      }

      throw new EntityValidationError(
        entity,
        issue.path.join("/"),
        issue.message
      );
    }
  };
}
