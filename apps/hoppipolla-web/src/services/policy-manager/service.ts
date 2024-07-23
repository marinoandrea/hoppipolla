export type Issuer = {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  name: string;
  default: boolean;
  description?: string;
};

export type Policy = {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  active: boolean;
  issuer: Issuer;
  title: string;
  statements: string;
  description?: string;
};

export type CreatePolicyInput = {
  statements: string;
  title?: string;
  description?: string;
};

export type UpdatePolicyInput = {
  issuer?: Issuer;
  title?: string;
  statements?: string;
  description?: string;
};

export interface IPolicyManager {
  publish(issuer: Issuer, input: CreatePolicyInput): Promise<Policy>;
  update(policyId: string, input: UpdatePolicyInput): Promise<Policy>;
  delete(policyId: string): Promise<void>;
  retrieve(policyId: string): Promise<Policy | null>;
  listAll(): Promise<Policy[]>;
  getDefaultIssuer(): Promise<Issuer>;
}
