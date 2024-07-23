"use server";

import { policyManager } from "@/services";
import {
  CreatePolicyInput,
  UpdatePolicyInput,
} from "@/services/policy-manager/service";

export async function getAllPolicies() {
  const policies = await policyManager.listAll();
  return policies.sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime());
}

export async function getDefaultIssuer() {
  return await policyManager.getDefaultIssuer();
}

export async function publishPolicy(data: CreatePolicyInput) {
  const defaultIssuer = await getDefaultIssuer();
  return await policyManager.publish(defaultIssuer, data);
}

export async function updatePolicy(id: string, data: UpdatePolicyInput) {
  return await policyManager.update(id, data);
}

export async function deletePolicy(id: string) {
  return await policyManager.delete(id);
}
