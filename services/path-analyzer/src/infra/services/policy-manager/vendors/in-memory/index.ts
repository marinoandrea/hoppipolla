import { Path } from "src/domain/entities";
import { IPolicyManager } from "src/domain/services";

export class InMemoryPolicyManagerClient implements IPolicyManager {
  private identityMap: Map<Path["id"], boolean>;
  private latestTimestamp: Date;

  constructor(
    identityMap: Map<string, boolean> = new Map(),
    latestTimestamp: Date = new Date()
  ) {
    this.identityMap = identityMap;
    this.latestTimestamp = latestTimestamp;
  }

  async getLatestPolicyTimestamp(): Promise<Date> {
    return this.latestTimestamp;
  }

  async validatePath(path: Path): Promise<boolean> {
    return this.identityMap.get(path.id) ?? false;
  }
}
