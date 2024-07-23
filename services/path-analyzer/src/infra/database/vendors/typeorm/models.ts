import {
  Column,
  CreateDateColumn,
  Entity,
  JoinColumn,
  ManyToOne,
  OneToMany,
  PrimaryColumn,
  UpdateDateColumn,
} from "typeorm";

import { IsdAs, PathStatus } from "src/domain/entities";

@Entity({ synchronize: false })
export abstract class BaseModel {
  @PrimaryColumn({ generated: "uuid" })
  id!: string;

  @CreateDateColumn()
  createdAt!: Date;

  @UpdateDateColumn()
  updatedAt!: Date;
}

@Entity({ name: "nodes" })
export class NodeModel extends BaseModel {
  @Column()
  isdAs!: IsdAs;

  @OneToMany(() => HopModel, (hop) => hop.path)
  hops!: HopModel[];
}

@Entity({ name: "paths" })
export class PathModel extends BaseModel {
  @Column({ unique: true })
  fingerprint!: string;

  @Column()
  src!: IsdAs;

  @Column()
  dst!: IsdAs;

  @Column()
  localIp!: string;

  @Column("int")
  mtuBytes!: number;

  @Column({
    type: "simple-enum",
    enum: PathStatus,
    default: PathStatus.UNKNOWN,
  })
  status!: PathStatus;

  @Column()
  expiresAt!: Date;

  @Column({ type: "datetime", nullable: true })
  lastValidatedAt!: Date | null;

  @Column({ default: false })
  valid!: boolean;

  @OneToMany(() => HopModel, (hop) => hop.path, {
    eager: true,
    cascade: ["insert"],
  })
  hops!: HopModel[];
}

@Entity({ name: "hops" })
export class HopModel extends BaseModel {
  @Column()
  inboundInterface!: number;

  @Column()
  outboundInterface!: number;

  @ManyToOne(() => NodeModel, { eager: true, cascade: ["insert"] })
  @JoinColumn({ name: "nodeId" })
  node!: NodeModel;

  @ManyToOne(() => PathModel, (path) => path.hops)
  @JoinColumn({ name: "pathId" })
  path!: PathModel;
}
