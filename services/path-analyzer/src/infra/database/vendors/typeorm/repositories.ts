import assert from "node:assert/strict";

import { Entity, Identifier, IsdAs, Node, Path } from "src/domain/entities";
import {
  IEntityRepository,
  INodeRepository,
  IPathRepository,
} from "src/domain/repositories";

import { AppDataSource } from ".";
import { InMemoryStore, REMOVED_SYMBOL } from "../utils";
import { BaseModel, NodeModel, PathModel } from "./models";

import { Repository } from "typeorm";

type Session = ReturnType<typeof AppDataSource.createQueryRunner>;

abstract class TypeOrmEntityRepository<
  TEntity extends Entity,
  TModel extends BaseModel,
> implements IEntityRepository<TEntity>
{
  store: InMemoryStore<TEntity>;
  repository: Repository<TModel>;
  session: Session;

  constructor(
    session: Session,
    repository: Repository<TModel>,
    store: InMemoryStore<TEntity> = new Map()
  ) {
    this.store = store;
    this.session = session;
    this.repository = repository;
  }

  public abstract mapEntityToModel(entity: TEntity): TModel;
  public abstract mapModelToEntity(model: TModel): TEntity;

  public async add(entity: TEntity): Promise<void> {
    const currentValue = this.store.get(entity.id);
    assert.notEqual(
      currentValue,
      undefined,
      `Entity ${entity} has already been added to the repository, modify the instance instead`
    );
    this.store.set(entity.id, entity);
    await this.session.manager
      .withRepository(this.repository)
      .save(this.mapEntityToModel(entity));
  }

  public async getById(id: Identifier): Promise<TEntity | null> {
    const entityOrRemoved = this.store.get(id);

    assert.notEqual(
      entityOrRemoved,
      REMOVED_SYMBOL,
      `Entity with id ${id} has been removed from the repository, your handle is not valid`
    );

    const entity = entityOrRemoved as TEntity | undefined;
    if (entity != null) {
      return entity;
    }

    const model = await this.session.manager
      .withRepository(this.repository)
      // @ts-expect-error TModel["id"] for some reason does not match the type
      // for Identifier
      .findOne({ where: { id } });

    if (!model) {
      return null;
    }

    return this.mapModelToEntity(model);
  }

  public async remove(entity: TEntity): Promise<void> {
    this.assertNotRemoved(entity);
    this.store.set(entity.id, REMOVED_SYMBOL);
    await this.session.manager
      .withRepository(this.repository)
      .remove(this.mapEntityToModel(entity));
  }

  private async persist(entity: TEntity): Promise<void> {
    this.assertNotRemoved(entity);
    const model = this.mapEntityToModel(entity);
    await this.session.manager.withRepository(this.repository).save(model);
  }

  public async persistAll(): Promise<void> {
    await Promise.all(
      Array.from(this.store.values())
        .filter((e) => !!e && e !== REMOVED_SYMBOL)
        .map(this.persist)
    );
  }

  private assertNotRemoved(entity: TEntity) {
    assert.notEqual(
      this.store.get(entity.id),
      REMOVED_SYMBOL,
      `Entity with ${entity} has been removed from the repository, your handle is not valid`
    );
  }
}

export class TypeOrmNodeRepository
  extends TypeOrmEntityRepository<Node, NodeModel>
  implements INodeRepository
{
  constructor(session: Session) {
    super(session, AppDataSource.getRepository(NodeModel));
  }

  public mapEntityToModel(entity: Node) {
    const model = new NodeModel();
    model.id = entity.id;
    model.createdAt = entity.createdAt;
    model.updatedAt = entity.updatedAt;
    model.isdAs = entity.isdAs;
    return model;
  }

  public mapModelToEntity(model: NodeModel) {
    return new Node(model);
  }

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

export class TypeOrmPathRepository
  extends TypeOrmEntityRepository<Path, PathModel>
  implements IPathRepository
{
  constructor(session: Session) {
    super(session, AppDataSource.getRepository(PathModel));
  }

  public mapEntityToModel(entity: Path) {
    const model = new PathModel();
    model.id = entity.id;
    model.createdAt = entity.createdAt;
    model.updatedAt = entity.updatedAt;
    model.fingerprint = entity.fingerprint;
    model.status = entity.status;
    model.src = entity.src;
    model.dst = entity.dst;
    model.localIp = entity.localIp;
    model.sequence = entity.sequence;
    model.mtuBytes = entity.mtuBytes;
    model.expiresAt = entity.expiresAt;
    model.lastValidatedAt = entity.lastValidatedAt;
    model.valid = entity.valid;
    return model;
  }

  public mapModelToEntity(model: PathModel) {
    return new Path({
      ...model,
      hops: model.hops.map((hopModel) => ({
        node: new Node(hopModel.node),
        inboundInterface: hopModel.inboundInterface,
        outboundInterface: hopModel.outboundInterface,
      })),
    });
  }

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
