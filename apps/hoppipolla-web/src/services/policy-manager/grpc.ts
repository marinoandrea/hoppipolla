import { credentials } from "@grpc/grpc-js";

import { google } from "@/protos/google/protobuf/empty";
import { hoppipolla as policyPb } from "@/protos/policy";

import { grpcCall } from "../grpc";
import {
  CreatePolicyInput,
  IPolicyManager,
  Issuer,
  Policy,
  UpdatePolicyInput,
} from "./service";

export class GrpcPolicyManager implements IPolicyManager {
  client: policyPb.policy.PolicyManagerClient;

  constructor(address: string) {
    try {
      this.client = new policyPb.policy.PolicyManagerClient(
        address,
        credentials.createInsecure()
      );
    } catch (e) {
      console.error(e);
      throw e;
    }
  }

  async publish(issuer: Issuer, input: CreatePolicyInput) {
    const req = new policyPb.policy.CreatePolicyRequest({
      ...input,
      issuer_id: issuer.id,
    });

    try {
      const res = await grpcCall(this.client.CreatePolicy, req);

      if (!res || !res.has_policy) {
        console.error("No response from policy-manager");
        throw new Error("No response from policy-manager");
      }

      return mapMessageToPolicy(res.policy);
    } catch (e) {
      console.error(e);
      throw e;
    }
  }

  async delete(policyId: string): Promise<void> {
    const req = new policyPb.policy.DeletePolicyRequest({ id: policyId });

    try {
      const res = await grpcCall(this.client.DeletePolicy, req);

      if (!res) {
        console.error("No response from policy-manager");
        throw new Error("No response from policy-manager");
      }
    } catch (e) {
      console.error(e);
      throw new Error("No response from policy-manager");
    }
  }

  async getDefaultIssuer(): Promise<Issuer> {
    const req = new google.protobuf.Empty();

    try {
      const res = await grpcCall(this.client.GetDefaultIssuer, req);

      if (!res || !res.has_issuer) {
        console.error("No response from policy-manager");
        throw new Error("No response from policy-manager");
      }

      return mapMessageToIssuer(res.issuer);
    } catch (e) {
      console.error(e);
      throw e;
    }
  }

  async listAll(): Promise<Policy[]> {
    const req = new google.protobuf.Empty();

    try {
      const res = await grpcCall(this.client.ListPolicies, req);

      if (!res) {
        console.error("No response from policy-manager");
        throw new Error("No response from policy-manager");
      }

      return res.policies.map(mapMessageToPolicy);
    } catch (e) {
      console.error(e);
      throw e;
    }
  }

  async update(policyId: string, input: UpdatePolicyInput): Promise<Policy> {
    const req = new policyPb.policy.UpdatePolicyRequest({
      ...input,
      id: policyId,
    });

    try {
      const res = await grpcCall(this.client.UpdatePolicy, req);

      if (!res || !res.has_policy) {
        console.error("No response from policy-manager");
        throw new Error("No response from policy-manager");
      }

      return mapMessageToPolicy(res.policy);
    } catch (e) {
      console.error(e);
      throw e;
    }
  }

  async retrieve(id: string): Promise<Policy | null> {
    const req = new policyPb.policy.GetPolicyRequest({ id });

    try {
      const res = await grpcCall(this.client.GetPolicy, req);

      if (!res) {
        console.error("No response from policy-manager");
        throw new Error("No response from policy-manager");
      }

      return mapMessageToPolicy(res.policy);
    } catch (e) {
      console.error(e);
      throw e;
    }
  }
}

function mapMessageToPolicy(message: policyPb.policy.Policy) {
  return {
    id: message.id,
    createdAt: new Date(message.created_at),
    updatedAt: new Date(message.created_at),
    active: message.active,
    title: message.title,
    statements: message.statements,
    description: message.description,
    issuer: mapMessageToIssuer(message.issuer),
  };
}

function mapMessageToIssuer(message: policyPb.policy.Issuer) {
  return {
    id: message.id,
    createdAt: new Date(message.created_at),
    updatedAt: new Date(message.created_at),
    default: message.default,
    name: message.name,
    description: message.description,
  };
}
