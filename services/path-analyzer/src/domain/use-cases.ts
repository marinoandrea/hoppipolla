import { Hop, Node, Path, validateIsdAsSchema } from "./entities";
import { INodeRepository, IPathRepository } from "./repositories";
import { IPolicyManager, IScionClient, ShowpathsPathResult } from "./services";

/**
 * Find a path for destination that complies with the policies currently
 * published on the Hoppipolla policy manager.
 */
export async function getPathForAddress(
  pathRepository: IPathRepository,
  nodeRepository: INodeRepository,
  policyManager: IPolicyManager,
  scionClient: IScionClient,
  destination: string
): Promise<Path | null> {
  if (!validateIsdAsSchema(destination)) {
    // TODO: better error
    throw new Error();
  }

  // query the database for already validated paths
  const latestPolicyTimestamp = await policyManager.getLatestPolicyTimestamp();

  const validPaths = await pathRepository.getValidPathsForDestination(
    destination,
    latestPolicyTimestamp
  );

  if (validPaths.length > 0) {
    return validPaths[0];
  }

  // query SCION daemon for potential new paths to reach destination
  const showpathsResults = await scionClient.showpaths(destination);
  const newPaths = await Promise.all(showpathsResults.map(buildPathFromResult));

  // validate the paths using the policy manager
  const validationStartTimestamp = new Date();
  await Promise.all(
    newPaths.map(async (path) => {
      const valid = await policyManager.validatePath(path);
      path.lastValidatedAt = validationStartTimestamp;
      path.valid = valid;
    })
  );

  await pathRepository.addAll(newPaths);

  return newPaths.find((path) => path.valid) ?? null;

  async function buildPathFromResult(
    result: ShowpathsPathResult
  ): Promise<Path> {
    const existingPath = await pathRepository.getByFingerprint(
      result.fingerprint
    );

    if (existingPath) {
      return existingPath;
    }

    const hops: Hop[] = [];
    for (let i = 0; i < result.hops.length; i++) {
      const isdAs = result.hops[i].isdAs;
      const inboundInterface = result.hops[i].inboundInterface;
      const outboundInterface = result.hops[i].outboundInterface;

      // find or create the ISD-AS node entity
      let node = await nodeRepository.getByIsdAs(isdAs);
      if (!node) {
        node = new Node({ isdAs });
        await nodeRepository.add(node);
      }

      hops.push({ node, inboundInterface, outboundInterface });
    }

    return new Path({ ...result, hops });
  }
}
