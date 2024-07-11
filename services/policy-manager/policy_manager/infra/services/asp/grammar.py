from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from policy_manager.domain.entities import (Hop, HopReading, Issuer, Path,
                                            Policy)


@dataclass
class HoppipollaSymbol(ABC):
    pass


@dataclass
class PathSymbol(HoppipollaSymbol):
    path: Path

    def __repr__(self) -> str:
        return f"path(\"{self.path.fingerprint}\")."


@dataclass
class HopSymbol(HoppipollaSymbol):
    hop: Hop

    def __repr__(self) -> str:
        return f"hop(\"{self.hop.isd_as}\")."


@dataclass
class HopReadingSymbol(HoppipollaSymbol):
    data: HopReading

    def __repr__(self) -> str:
        out = f"data(\"{self.data["id"]}\")."
        for name in self.data:
            if name == "id":
                continue

            value = self.data[name]

            if isinstance(value, datetime):
                out += f"\n{name}(\"{self.data["id"]}\", {
                    int(value.timestamp() * 1000)})."
            elif type(value) is int:
                out += f"\n{name}(\"{self.data["id"]}\", {value})."
            else:
                out += f"\n{name}(\"{self.data["id"]}\", \"{value}\")."

        return out


@dataclass
class ContainsSymbol(HoppipollaSymbol):
    path: Path
    hop: Hop

    def __repr__(self) -> str:
        return f"contains(\"{self.path.fingerprint}\", \"{self.hop.isd_as}\")."


@dataclass
class CollectedSymbol(HoppipollaSymbol):
    hop: Hop
    data: HopReading

    def __repr__(self) -> str:
        return f"collected(\"{self.hop.isd_as}\", \"{self.data["id"]}\")."


@dataclass
class PolicySymbol(HoppipollaSymbol):
    policy: Policy

    def __repr__(self) -> str:
        out = f"policy(\"{self.policy.id}\").\n"
        out += f"has_issued(\"{self.policy.issuer.id}\", \"{self.policy.id}\")"
        return out


@dataclass
class IssuerSymbol(HoppipollaSymbol):
    issuer: Issuer

    def __repr__(self) -> str:
        return f"issuer(\"{self.issuer.id}\").\n"


@dataclass
class OverpowersSymbol(HoppipollaSymbol):
    policy_a: Policy
    policy_b: Policy

    def __repr__(self) -> str:
        return f"overpowers(\"{self.policy_a.id}\", \"{self.policy_b.id}\")."
