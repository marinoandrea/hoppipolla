import { getAllPolicies } from "@/actions/policies";
import PolicyList from "@/features/policies/policy-list";
import PolicyProfile from "@/features/policies/policy-profile";
import { notFound } from "next/navigation";

export default async function PoliciesPolicyId({
  params,
}: {
  params: { policyId: string };
}) {
  const policies = await getAllPolicies();
  const policy = policies.find((p) => p.id === params.policyId);

  if (!policy) {
    notFound();
  }

  return (
    <div className="grid grid-cols-6 divide-x">
      <div className="col-span-2 overflow-y-auto h-[calc(100vh-64px)]">
        <PolicyList policies={policies} currentPolicy={policy} />
      </div>
      <div className="col-span-4 p-4">
        <PolicyProfile policy={policy} />
      </div>
    </div>
  );
}
