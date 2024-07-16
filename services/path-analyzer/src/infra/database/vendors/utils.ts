import { Entity, Identifier } from "src/domain/entities";

export const REMOVED_SYMBOL = Symbol("REMOVED");

export type InMemoryStore<TEntity extends Entity> = Map<
  Identifier,
  TEntity | typeof REMOVED_SYMBOL
>;
