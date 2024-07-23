import { Entity, Identifier, IsdAs, Node, Path } from "src/domain/entities";
import {
  IEntityRepository,
  INodeRepository,
  IPathRepository,
} from "src/domain/repositories";

import { AppDataSource } from ".";
import { BaseModel, HopModel, NodeModel, PathModel } from "./models";

import { LessThan, MoreThan, QueryRunner, Repository } from "typeorm";

type Session = QueryRunner;

abstract class TypeOrmEntityRepository<
  TEntity extends Entity,
  TModel extends BaseModel,
> implements IEntityRepository<TEntity>
{
  repository: Repository<TModel>;
  session: Session;

  constructor(session: Session, repository: Repository<TModel>) {
    this.session = session;
    this.repository = repository;
  }

  public abstract mapEntityToModel(entity: TEntity): TModel;
  public abstract mapModelToEntity(model: TModel): TEntity;

  public async add(entity: TEntity): Promise<void> {
    this.session.manager
      .withRepository(this.repository)
      .save(this.mapEntityToModel(entity));
  }

  public async addAll(entities: TEntity[]): Promise<void> {
    this.session.manager
      .withRepository(this.repository)
      .save(entities.map(this.mapEntityToModel));
  }

  public async getById(id: Identifier): Promise<TEntity | null> {
    const model = await this.session.manager
      .withRepository(this.repository)
      // @ts-expect-error TModel["id"] for some reason does not match the type
      // for Identifier
      .findOne({ where: { id }, loadEagerRelations: true });

    if (!model) {
      return null;
    }

    return this.mapModelToEntity(model);
  }

  public async remove(entity: TEntity): Promise<void> {
    await this.session.manager
      .withRepository(this.repository)
      .remove(this.mapEntityToModel(entity));
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

  public async getByIsdAs(isdAs: IsdAs): Promise<Node | null> {
    const model = await this.session.manager
      .withRepository(this.repository)
      .findOne({ where: { isdAs } });

    if (!model) {
      return null;
    }

    return this.mapModelToEntity(model);
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
    model.mtuBytes = entity.mtuBytes;
    model.expiresAt = entity.expiresAt;
    model.lastValidatedAt = entity.lastValidatedAt;
    model.valid = entity.valid;

    model.hops = entity.hops.map((h) => {
      const hModel = new HopModel();

      hModel.node = hModel.node = new NodeModel();
      hModel.node.id = h.node.id;
      hModel.node.createdAt = h.node.createdAt;
      hModel.node.updatedAt = h.node.updatedAt;
      hModel.node.isdAs = h.node.isdAs;

      hModel.inboundInterface = h.inboundInterface;
      hModel.outboundInterface = h.outboundInterface;

      return hModel;
    });

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

  public async getByFingerprint(fingerprint: string): Promise<Path | null> {
    const model = await this.session.manager
      .withRepository(this.repository)
      .findOne({ where: { fingerprint } });

    if (!model) {
      return null;
    }

    return this.mapModelToEntity(model);
  }

  public async getValidPathsForDestination(
    dst: IsdAs,
    minValidationTimestamp: Date
  ): Promise<Path[]> {
    const models = await this.session.manager
      .withRepository(this.repository)
      .find({
        where: {
          dst,
          lastValidatedAt: MoreThan(minValidationTimestamp),
          expiresAt: LessThan(new Date()),
          valid: true,
        },
      });

    return models.map(this.mapModelToEntity);
  }
}
