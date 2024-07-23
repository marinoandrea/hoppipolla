"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Policy } from "@/services/policy-manager/service";

interface IPolicyListProps {
  policies: Policy[];
  currentPolicy?: Policy;
}

export default function PolicyList({
  policies,
  currentPolicy,
}: IPolicyListProps) {
  return (
    <div className="flex flex-col divide-y divide-foreground">
      {policies.map((p) => (
        <PolicyItem
          key={p.id}
          policy={p}
          isSelected={currentPolicy?.id === p.id}
        />
      ))}
    </div>
  );
}

function PolicyItem({
  policy,
  isSelected,
}: {
  policy: Policy;
  isSelected: boolean;
}) {
  const [isHovered, setIsHovered] = useState(false);

  const router = useRouter();

  return (
    <div
      key={policy.id}
      onClick={() => router.push(`/policies/${policy.id}`)}
      className={`p-4 flex flex-col gap-2 cursor-pointer transition-colors ${
        isHovered ? "text-primary" : undefined
      } ${isSelected ? "bg-foreground" : undefined}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <p className="font-bold">{policy.title}</p>
      <p className="text-sm text-ellipsis line-clamp-1">{policy.description}</p>
      <p className="text-xs">Updated: {policy.updatedAt.toLocaleString()}</p>
      <p className="text-xs">Issuer: {policy.issuer.name}</p>
    </div>
  );
}
