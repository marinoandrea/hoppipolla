import { IpAddress, IsdAs, Path, PathStatus } from "./entities";

/**
 * Interface for the external Hoppipolla policy manager service.
 * */
export interface IPolicyManager {
  /**
   * Retrieve the timestamp at which the last policy was published.
   * */
  getLatestPolicyTimestamp(): Promise<Date>;
  /**
   * Check whether a given path is compliant with the published policies.
   * @param path The path to validate
   */
  validatePath(path: Path): Promise<boolean>;
}

export type ShowpathsPathResult = {
  fingerprint: string;
  status: PathStatus;
  sequence: string;
  dst: IsdAs;
  src: IsdAs;
  localIp: IpAddress;
  expiry: Date;
  mtuBytes: number;
  hops: {
    isdAs: IsdAs;
    inboundInterface: number;
    outboundInterface: number;
  }[];
};

export interface IScionClient {
  showpaths(dst: IsdAs): Promise<ShowpathsPathResult[]>;
}
