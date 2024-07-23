import childPrcess from "child_process";
import { promisify } from "util";
import { z } from "zod";

import { config } from "src/config";
import { IpAddress, IsdAs, PathStatus } from "src/domain/entities";
import { InternalError } from "src/domain/errors";
import { IScionClient, ShowpathsPathResult } from "src/domain/services";
import logger from "src/logging";

const exec = promisify(childPrcess.exec);

/** Object return from `scion showpaths` command in JSON format. */
export type ShowpathsOutput = z.infer<typeof showpathsOutputSchema>;

export class ScionSubprocessClient implements IScionClient {
  private sciondAddress: string;

  constructor(sciondAddress: string) {
    this.sciondAddress = sciondAddress;
  }

  /**
   * Returns an object containing SCION paths for given destination.
   * @param destination ISD-AS tuple
   * @param maxPaths Maximum number of paths to return
   * @returns Paths information
   */
  async showpaths(destination: string): Promise<ShowpathsPathResult[]> {
    const command = [
      `${config.SCION_EXE_PATH} showpaths`,
      "--format json",
      "--extended",
      `--sciond ${this.sciondAddress}`,
      `--maxpaths ${config.MAX_PATHS_BATCH}`,
      destination,
    ];

    logger.debug(`Executing sciond showpaths as ${this.sciondAddress}`);

    try {
      const { stdout } = await exec(command.join(" "));
      const json = JSON.parse(stdout);
      const result = await showpathsOutputSchema.safeParseAsync(json);

      // the result is missing paths if sciond does not find paths
      if (!result.success) {
        return [];
      }

      // TODO: validate string addresses
      return result.data.paths.map((path) => ({
        fingerprint: path.fingerprint,
        status: statusToEnum(path.status),
        src: result.data.local_isd_as as IsdAs,
        dst: result.data.destination as IsdAs,
        localIp: path.local_ip as IpAddress,
        expiry: path.expiry,
        sequence: path.sequence,
        mtuBytes: path.mtu,
        hops: parseHops(path),
      }));
    } catch (e) {
      logger.debug(e);
      throw new InternalError(`Cannot execute showpaths: ${e}`);
    }

    function statusToEnum(status: string) {
      switch (status) {
        case "alive":
          return PathStatus.ALIVE;
        case "timeout":
          return PathStatus.TIMEOUT;
        default:
          return PathStatus.UNKNOWN;
      }
    }

    function parseHops(path: ShowpathsOutput["paths"][0]) {
      const hops: ShowpathsPathResult["hops"] = [];

      for (let i = 0; i < path.hops.length; i++) {
        const ifId = path.hops[i].ifid;
        const hopInterface =
          typeof ifId === "number" ? ifId : Number.parseInt(ifId);
        const isdAs = path.hops[i].isd_as as IsdAs;

        // if this is the second instance of the ISD-AS, consider interface as outbound
        if (i > 0 && hops[i - 1]?.isdAs == isdAs) {
          hops[i - 1].outboundInterface = hopInterface;
          continue;
        }

        // if this is the first hop, consider interface as outbound
        if (i == 0) {
          hops.push({
            isdAs,
            inboundInterface: 0,
            outboundInterface: hopInterface,
          });
          continue;
        }

        // otherwise consider interface as inbound
        hops.push({
          isdAs,
          inboundInterface: hopInterface,
          outboundInterface: 0,
        });
      }

      return hops;
    }
  }
}

// this schema is only used for sanity purposes, parsing is not expected to fail
const showpathsOutputSchema = z.object({
  local_isd_as: z.string(),
  destination: z.string(),
  paths: z.array(
    z.object({
      fingerprint: z.string(),
      hops: z.array(
        z.object({
          ifid: z.number().int(),
          isd_as: z.string(),
        })
      ),
      sequence: z.string(),
      next_hop: z.string(),
      expiry: z.coerce.date(),
      mtu: z.number().positive(),
      latency: z.array(z.number()).optional().nullable(),
      carbon_intensity: z.array(z.number()).optional().nullable(),
      // see https://github.com/scionproto/scion/blob/eacdeef5732b67dd5fda83f2cf28bef33c3a9f8d/private/app/path/pathprobe/paths.go#L44
      status: z.enum(["timeout", "alive", "unknown"]),
      local_ip: z.string().ip(),
    })
  ),
});
