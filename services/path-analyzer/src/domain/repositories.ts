import { Entity, Identifier, IsdAs, Node, Path } from "./entities";

/**
 * Abstract interface for an implementation of the repository pattern for a
 * specific entity.
 */
export interface IEntityRepository<TEntity extends Entity> {
  /**
   * Add a new entity to the repository or modify the entity with the same identifier.
   * @param entity The entity to create/update
   */
  add(entity: TEntity): Promise<void>;
  /**
   * Remove an entity from the repository.
   * @param entity The entity to create/update
   */
  remove(entity: TEntity): Promise<void>;
  /**
   * Retrieve an entity with the specified identifier.
   * @param entity The entity to create/update
   */
  getById(id: Identifier): Promise<TEntity | null>;
}

export interface IPathRepository extends IEntityRepository<Path> {
  /**
   * Retrieve all the `Path` entities with `valid` set to true that have the
   * provided destination address.
   *
   * In order for a path to be valid it also has to not be expired.
   *
   * @param dst The ISD-AS destination address
   * @param minValidationTimestamp The minimum accepted value for `validatedAt`
   *  */
  getValidPathsForDestination(
    dst: IsdAs,
    minValidationTimestamp: Date
  ): Promise<Path[]>;

  /**
   * Retrieve a path based on its unique fingerprint hash.
   *
   * @param fingerprint The unique fingerprint of the path
   */
  getByFingerprint(fingerprint: string): Promise<Path | null>;
}

export interface INodeRepository extends IEntityRepository<Node> {
  /**
   * Retrieve a path based on its unique ISD-AS address.
   *
   * @param isdAs The unique ISD-AS address
   */
  getByIsdAs(isdAs: IsdAs): Promise<Node | null>;
}
