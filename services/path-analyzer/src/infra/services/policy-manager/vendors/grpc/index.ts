import grpc, {
  ClientUnaryCall,
  ServiceError,
  credentials,
} from "@grpc/grpc-js";
import { promisify } from "util";

import { Path } from "src/domain/entities";
import { InternalError } from "src/domain/errors";
import { IPolicyManager } from "src/domain/services";
import logger from "src/logging";
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

    return new Date(res.timestamp);
  }

  async validatePath(path: Path): Promise<boolean> {
    const req = new policyPb.policy.ValidatePathRequest({
      path: new pathPb.path.Path({
        dst_isd_as: path.dst,
        src_isd_as: path.src,
        expiration: path.expiresAt.toISOString(),
        mtu: path.mtuBytes,
        fingerprint: path.fingerprint,
        sequence: path.sequence,
        hops: path.hops.map(
          (hop) =>
            new pathPb.path.Hop({
              isd_as: hop.node.isdAs,
              inbound_interface: hop.inboundInterface,
              outbound_interface: hop.outboundInterface,
            })
        ),
      }),
    });

    try {
      const res = await call(this.client.ValidatePath, req);

      if (!res) {
        logger.error("No response from policy-manager");
        throw new InternalError("No response from policy-manager");
      }

      return res.valid;
    } catch (e) {
      logger.error("No response from policy-manager");
      throw new InternalError("No response from policy-manager");
    }
  }
}
