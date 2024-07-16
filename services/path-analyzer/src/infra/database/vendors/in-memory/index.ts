import { Entity, Identifier, IsdAs, Node, Path } from "src/domain/entities";
import {
  IEntityRepository,
  INodeRepository,
  IPathRepository,
} from "src/domain/repositories";

import assert from "node:assert/strict";

import { InMemoryStore, REMOVED_SYMBOL } from "../utils";

abstract class InMemoryEntityRepository<TEntity extends Entity>
  implements IEntityRepository<TEntity>
{
  store: InMemoryStore<TEntity>;

  constructor(store: InMemoryStore<TEntity> = new Map()) {
    this.store = store;
  }

  public add(entity: TEntity): Promise<void> {
    assert.notEqual(
      this.store.get(entity.id),
      undefined,
      `Entity ${entity} has already been added to the repository, modify the instance instead`
    );
    this.store.set(entity.id, entity);
    return Promise.resolve();
  }

  public getById(id: Identifier): Promise<TEntity | null> {
    const entityOrRemoved = this.store.get(id);
    assert.notEqual(
      entityOrRemoved,
      REMOVED_SYMBOL,
      `Entity with id ${id} has been removed from the repository, your handle is not valid`
    );
    const entity = entityOrRemoved as TEntity | undefined;
    return Promise.resolve(!entity ? null : entity);
  }

  public remove(entity: TEntity): Promise<void> {
    assert.notEqual(
      this.store.get(entity.id),
      REMOVED_SYMBOL,
      `Entity with ${entity} has already been removed from the repository, your handle is not valid`
    );
    this.store.set(entity.id, REMOVED_SYMBOL);
    return Promise.resolve();
  }

  public persist(entity: TEntity): Promise<void> {
    console.debug(`persisting ${entity}`);
    return Promise.resolve();
  }

  public async persistAll(): Promise<void> {
    await Promise.all(
      Array.from(this.store.values())
        .filter((e) => !!e && e !== REMOVED_SYMBOL)
        .map(this.persist)
    );
  }
}

export class InMemoryNodeRepository
  extends InMemoryEntityRepository<Node>
  implements INodeRepository
{
  public getByIsdAs(isdAs: IsdAs): Promise<Node | null> {
    for (const value of this.store.values()) {
      if (value === REMOVED_SYMBOL) {
        continue;
      }
      if (value.isdAs === isdAs) {
        return Promise.resolve(value);
      }
    }
    return Promise.resolve(null);
  }
}

export class InMemoryPathRepository
  extends InMemoryEntityRepository<Path>
  implements IPathRepository
{
  public getByFingerprint(fingerprint: string): Promise<Path | null> {
    for (const value of this.store.values()) {
      if (value === REMOVED_SYMBOL) {
        continue;
      }
      if (value.fingerprint === fingerprint) {
        return Promise.resolve(value);
      }
    }
    return Promise.resolve(null);
  }

  public getValidPathsForDestination(
    dst: IsdAs,
    minValidationTimestamp: Date
  ): Promise<Path[]> {
    const paths = [];
    for (const value of this.store.values()) {
      if (value === REMOVED_SYMBOL) {
        continue;
      }
      if (
        value.dst === dst &&
        value.valid &&
        value.lastValidatedAt &&
        value.lastValidatedAt >= minValidationTimestamp
      ) {
        paths.push(value);
      }
    }
    return Promise.resolve(paths);
  }
}
