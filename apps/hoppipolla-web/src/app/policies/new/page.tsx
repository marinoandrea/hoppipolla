import { getAllPolicies, publishPolicy } from "@/actions/policies";
import PublishPolicyForm from "@/features/policies/forms/publish-policy";
import PolicyList from "@/features/policies/policy-list";

export default async function PoliciesNew() {
  const policies = await getAllPolicies();

  return (
    <div className="grid grid-cols-6 divide-x">
      <div className="col-span-2 overflow-y-auto h-[calc(100vh-64px)]">
        <PolicyList policies={policies} />
      </div>
      <div className="col-span-4 p-6 flex flex-col gap-4">
        <h1 className="text-xl font-bold">Create New Policy</h1>
        <PublishPolicyForm publishAction={publishPolicy} />
      </div>
    </div>
  );
}
