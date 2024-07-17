import {
  Column,
  CreateDateColumn,
  Entity,
  JoinTable,
  ManyToMany,
  ManyToOne,
  OneToMany,
  PrimaryColumn,
  UpdateDateColumn,
} from "typeorm";

import { PathStatus } from "src/domain/entities";

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
  isdAs!: string;

  @OneToMany(() => HopModel, (hop) => hop.node)
  hops!: HopModel[];
}

@Entity({ name: "paths" })
export class PathModel extends BaseModel {
  @Column({ unique: true })
  fingerprint!: string;

  @Column()
  src!: string;

  @Column()
  dst!: string;

  @Column()
  localIp!: string;

  @Column("int")
  mtuBytes!: number;

  @Column()
  sequence!: string;

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

  @ManyToMany(() => HopModel, (hop) => hop.paths)
  hops!: HopModel[];
}

@Entity({ name: "hops" })
export class HopModel {
  @PrimaryColumn({ default: 0 })
  inboundInterface!: number;

  @PrimaryColumn({ default: 0 })
  outboundInterface!: number;

  @PrimaryColumn()
  nodeId!: string;

  @ManyToOne(() => NodeModel, (node) => node.hops)
  @JoinTable()
  node!: NodeModel;

  @ManyToMany(() => PathModel, (path) => path.hops)
  paths!: PathModel[];
}
