import { ServerUnaryCall, sendUnaryData } from "@grpc/grpc-js";

import { google as googleTimestamp } from "./protos/google/protobuf/timestamp";
import { hoppipolla as hoppipollaPath } from "./protos/path";
import { PathAnalyzerService } from "./service";

export class PathAnalyzerGrpcService extends hoppipollaPath.path
  .UnimplementedPathAnalyzerService {
  GetPathForAddr(
    call: ServerUnaryCall<
      hoppipollaPath.path.GetPathForAddrRequest,
      hoppipollaPath.path.GetPathForAddrResponse
    >,
    callback: sendUnaryData<hoppipollaPath.path.GetPathForAddrResponse>
  ): void {
    (async () => {
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
          expiration: new googleTimestamp.protobuf.Timestamp({
            seconds: output.expiresAt.getTime() / 1000,
          }),
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
    })()
      .then((res) => callback(null, res))
      .catch((err) => callback(err));
  }
}