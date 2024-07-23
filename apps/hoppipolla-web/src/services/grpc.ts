import { ClientUnaryCall, ServiceError } from "@grpc/grpc-js";
import { promisify } from "util";

const grpc = require("@grpc/grpc-js");

// NOTE: async/await is not supported, see https://github.com/grpc/grpc-node/issues/54
type Call<Input, Ret> = (
  input: Input,
  callback: (err: ServiceError | null, ret?: Ret) => void
) => ClientUnaryCall;

export const grpcCall = <Input, Ret>(
  call: Call<Input, Ret>,
  input: Input
): Promise<Ret | undefined> => promisify(call).call(grpc, input);
