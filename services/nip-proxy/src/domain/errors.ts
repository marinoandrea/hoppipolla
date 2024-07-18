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
