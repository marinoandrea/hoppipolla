import { v7 as uuidv7 } from "uuid";
import { z } from "zod";

import { EntityValidationError, handleZodValidation } from "./errors";

/** A unique identifier for the domain entities. */
export type Identifier = string;
/** A function that generates unique identifiers for the domain. */
export const generateIdentifier = uuidv7;

const identifierSchema = z.string().uuid().default(generateIdentifier);

/** String specialization for Ip addresses */
export type IpAddress = IpV4Address | IpV6Address;
type IpV4Address = `${number}.${number}.${number}.${number}`;
type IpV6Address =
  `${string}:${string}:${string}:${string}:${string}:${string}:${string}:${string}`;

/** String specialization for ISD-AS tuple addresses */
export type IsdAs = `${number}-${string}:${string}:${string}`;
const isdAsSchema = z
  .string()
  .regex(
    /^[0-9]+-([0-9a-fA-F]{1,4}:){2}[0-9a-fA-F]{1,4}$/,
    "invalid ISD-AS tuple"
  );

export const validateIsdAs = handleZodValidation("isdAs", isdAsSchema);

const dateInThePastSchema = z
  .date()
  .refine((d) => d <= new Date(), { message: "date cannot be in the future" });

const entityInputSchema = z
  .object({
    id: identifierSchema,
    createdAt: dateInThePastSchema.default(() => new Date()),
    updatedAt: dateInThePastSchema.default(() => new Date()),
  })
  .refine((input) => input.createdAt <= input.updatedAt, {
    message: "updatedAt cannot be before createdAt",
    path: ["createdAt"],
  });

const validateEntity = handleZodValidation("Entity", entityInputSchema);

type EntityInput = typeof entityInputSchema._input;

/** Represents an abstract entity in the domain. */
export abstract class Entity {
  private _id: Identifier;
  private _createdAt: Date;
  private _updatedAt: Date;

  constructor(data: EntityInput) {
    const validationResult = validateEntity(data);
    this._id = validationResult.id;
    this._createdAt = validationResult.createdAt;
    this._updatedAt = validationResult.updatedAt;
  }

  /** Unique identifier for the entity */
  public get id(): string {
    return this._id;
  }

  /** Creation timestamp for the entity */
  public get createdAt(): Date {
    return this._createdAt;
  }

  /** Last modification timestamp for the entity */
  public get updatedAt(): Date {
    return this._updatedAt;
  }

  public set updatedAt(value: Date) {
    const now = new Date();
    if (value < this._createdAt) {
      throw new EntityValidationError(
        "Entity",
        "updatedAt",
        "updatedAt cannot be before createdAt"
      );
    } else if (value > now) {
      throw new EntityValidationError(
        "Entity",
        "updatedAt",
        "updatedAt cannot be in the future"
      );
    }
    this._updatedAt = value;
  }
}

const nodeInputSchema = z.object({ isdAs: isdAsSchema });

export const validateNodeInput = handleZodValidation("Node", nodeInputSchema);

type NodeInput = EntityInput & typeof nodeInputSchema._input;

/** Node (Autonomous System) in the SCION network. */
export class Node extends Entity {
  private _isdAs: IsdAs;

  constructor(data: NodeInput) {
    super(data);
    const validationResult = validateNodeInput(data);
    this._isdAs = validationResult.data.isdAs as IsdAs;
  }

  /** ISD-AS address for the path hop */
  public get isdAs() {
    return this._isdAs;
  }
}

export enum PathStatus {
  UNKNOWN = "unknown",
  ALIVE = "alive",
  TIMEOUT = "timeout",
}

export type Hop = {
  node: Node;
  inboundInterface: number;
  outboundInterface: number;
};

const hopInterfaceSchema = z.coerce.number().int().gte(0).default(0);

const pathInputSchema = z.object({
  fingerprint: z.string(),
  src: isdAsSchema,
  dst: isdAsSchema,
  localIp: z.string().ip(),
  mtuBytes: z.number().int().gte(0).default(0),
  status: z.nativeEnum(PathStatus).default(PathStatus.UNKNOWN),
  expiresAt: dateInThePastSchema.default(() => new Date()),
  lastValidatedAt: dateInThePastSchema.nullable().default(null),
  valid: z.boolean().default(false),
  // TODO: validate the list so that it matches the sequence string
  hops: z.array(
    z.object({
      node: z.instanceof(Node),
      inboundInterface: hopInterfaceSchema,
      outboundInterface: hopInterfaceSchema,
    })
  ),
});

export const validatePathInput = handleZodValidation("Path", pathInputSchema);

type PathInput = EntityInput & typeof pathInputSchema._input;

/** Path in the SCION network between source ISD-AS and destination ISD-AS. */
export class Path extends Entity {
  private _fingerprint: string;
  private _src: IsdAs;
  private _dst: IsdAs;
  private _localIp: IpAddress;
  private _mtuBytes: number;
  private _status: PathStatus;
  private _expiresAt: Date;
  private _lastValidatedAt: Date | null = null;
  private _valid: boolean = false;
  private _hops: Hop[] = [];

  constructor(data: PathInput) {
    super(data);

    const validationResult = validatePathInput(data);

    this._fingerprint = validationResult.data.fingerprint;
    this._src = validationResult.data.src as IsdAs;
    this._dst = validationResult.data.dst as IsdAs;
    this._localIp = validationResult.data.localIp as IpAddress;
    this._mtuBytes = validationResult.data.mtuBytes;
    this._expiresAt = validationResult.data.expiresAt;
    this._status = validationResult.data.status;
    this._lastValidatedAt = validationResult.data.lastValidatedAt;
    this._valid = validationResult.data.valid;
    this._hops = validationResult.data.hops;
  }

  /** Unique fingerprint of the path */
  public get fingerprint() {
    return this._fingerprint;
  }

  /** The source ISD-AS of the path */
  public get src() {
    return this._src;
  }

  /** The destination ISD-AS of the path */
  public get dst() {
    return this._dst;
  }

  /** The local IP of the path source host */
  public get localIp() {
    return this._localIp;
  }

  /**
   * Maximum transmission unit (MTU).
   * Number of bytes of the largest data packets accepted on the path
   */
  public get mtuBytes() {
    return this._mtuBytes;
  }

  /**
   * Path string representation for hops as space separated tuples in the form ISD-AS#IF,IF.
   */
  public get sequence() {
    return this.hops
      .map(
        (hop) =>
          `${hop.node.isdAs}#${hop.inboundInterface},${hop.outboundInterface}`
      )
      .join(" ");
  }

  /**
   * Status of the path based on probing (active, timeout, or unknown).
   */
  public get status() {
    return this._status;
  }

  /**
   * Times of expiration of the path.
   * SCION does not guarantee this path to be viable after this timestamp.
   */
  public get expiresAt() {
    return this._expiresAt;
  }

  /**
   * Times of latest Hoppipolla policy manager validation run on this path.
   * The path should not be considered to comply with the policies if it was
   * validated before the latest update of the policy manager state.
   *
   * It is `null` if the path was never validated before.
   */
  public get lastValidatedAt(): Date | null {
    return this._lastValidatedAt;
  }

  public set lastValidatedAt(value: Date) {
    const now = new Date();
    if (value < this.createdAt) {
      throw new EntityValidationError(
        "Path",
        "lastValidatedAt",
        "lastValidatedAt cannot be before createdAt"
      );
    } else if (value > now) {
      throw new EntityValidationError(
        "Path",
        "lastValidatedAt",
        "lastValidatedAt cannot be in the future"
      );
    }
    this._lastValidatedAt = value;
  }

  /**
   * Whether this path was deemed compliant with the policies by the Hoppipolla
   * policy manager. It is `false` even if the path was never validated.
   */
  public get valid() {
    return this._valid;
  }

  public set valid(value: boolean) {
    if (value && !this._lastValidatedAt) {
      throw new EntityValidationError(
        "Path",
        "valid",
        "cannot set a path to valid without a validation timestamp"
      );
    }
    this._valid = value;
  }

  /**
   * List of network hops for the path, including ISD-AS, inbound interface,
   * and outbound interface.
   */
  public get hops() {
    return this._hops;
  }
}
