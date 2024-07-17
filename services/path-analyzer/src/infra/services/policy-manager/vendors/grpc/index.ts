import grpc, {
  ClientUnaryCall,
  ServiceError,
  credentials,
} from "@grpc/grpc-js";
import { promisify } from "util";

import { Path } from "src/domain/entities";
import { IPolicyManager } from "src/domain/services";
import { google as googlePbEmpty } from "src/protos/google/protobuf/empty";
import { hoppipolla as pathPb } from "src/protos/path";
import { hoppipolla as policyPb } from "src/protos/policy";

// NOTE: async/await is not supported, see https://github.com/grpc/grpc-node/issues/54
type Call<Input, Ret> = (
  input: Input,
  callback: (err: ServiceError | null, ret?: Ret) => void
) => ClientUnaryCall;

export const call = <Input, Ret>(
  call: Call<Input, Ret>,
  input: Input
): Promise<Ret | undefined> => promisify(call).call(grpc, input);

export class PolicyManagerGrpcClient implements IPolicyManager {
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

  async getLatestPolicyTimestamp(): Promise<Date> {
    const req = new googlePbEmpty.protobuf.Empty();
    const res = await call(this.client.GetLatestPolicyTimestamp, req);

    if (!res) {
      throw new Error();
    }

    return new Date(res.timestamp.seconds);
  }

  async validatePath(path: Path): Promise<boolean> {
    const req = new policyPb.policy.ValidatePathRequest({
      path: new pathPb.path.Path({ ...path }),
    });
    const res = await call(this.client.ValidatePath, req);

    if (!res) {
      throw new Error();
    }

    return res.valid;
  }
}
