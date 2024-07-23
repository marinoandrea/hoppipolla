import { config } from "@/config";

import { GrpcPolicyManager } from "./policy-manager/grpc";
import { IPolicyManager } from "./policy-manager/service";

export const policyManager: IPolicyManager = new GrpcPolicyManager(
  config.POLICY_MANAGER_URI
);
