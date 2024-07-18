import { expect, test } from "@jest/globals";
import { EntityValidationError } from "src/domain/errors";
import { getPathForAddress } from "src/domain/use-cases";
import {
  InMemoryNodeRepository,
  InMemoryPathRepository,
} from "src/infra/database/vendors/in-memory";
import { InMemoryPolicyManagerClient } from "src/infra/services/policy-manager/vendors/in-memory";
import { InMemoryScionClient } from "src/infra/services/scion-client/vendors/in-memory";

test("throws an error when the ISD-AS destination is malformed", async () => {
  const pathRepository = new InMemoryPathRepository();
  const nodeRepository = new InMemoryNodeRepository();
  const policyManager = new InMemoryPolicyManagerClient();
  const scionClient = new InMemoryScionClient();
  try {
    await getPathForAddress(
      pathRepository,
      nodeRepository,
      policyManager,
      scionClient,
      "malformed-isd-as"
    );
  } catch (e) {
    expect(e).toBeInstanceOf(EntityValidationError);
    const eSpecific = e as EntityValidationError;
    expect(eSpecific.entity).toBe("isdAs");
  }
});
