import { ServerUnaryCall, sendUnaryData } from "@grpc/grpc-js";

import logger from "./logging";
import { hoppipolla as hoppipollaPath } from "./protos/path";
import { PathAnalyzerService } from "./service";

function execute<TRequest, TResponse>(
  call: ServerUnaryCall<TRequest, TResponse>,
  callback: sendUnaryData<TResponse>,
  func: () => Promise<TResponse>
) {
  func()
    .then((res) => {
      logger.info(`${call.getPath()} OK`);
      logger.debug(`Response: ${res}`);
      callback(null, res);
    })
    .catch((err) => {
      logger.error(`${call.getPath()} ERROR`);
      logger.debug(`Error: ${err}`);
      callback(err, null);
    });
}

export class PathAnalyzerGrpcService extends hoppipollaPath.path
  .UnimplementedPathAnalyzerService {
  GetPathForAddr(
    call: ServerUnaryCall<
      hoppipollaPath.path.GetPathForAddrRequest,
      hoppipollaPath.path.GetPathForAddrResponse
    >,
    callback: sendUnaryData<hoppipollaPath.path.GetPathForAddrResponse>
  ): void {
    execute(call, callback, async () => {
      const response = new hoppipollaPath.path.GetPathForAddrResponse();

      const output = await PathAnalyzerService.executeGetPathForAddress(
        call.request.destination
      );

      if (output) {
        response.path = new hoppipollaPath.path.Path({
          fingerprint: output.fingerprint,
          dst_isd_as: output.dst,
          src_isd_as: output.src,
          sequence: output.sequence,
          mtu: output.mtuBytes,
          expiration: output.expiresAt.toISOString(),
          hops: output.hops.map(
            (hop) =>
              new hoppipollaPath.path.Hop({
                isd_as: hop.node.isdAs,
                inbound_interface: hop.inboundInterface,
                outbound_interface: hop.outboundInterface,
              })
          ),
        });
      }

      return response;
    });
  }
}
