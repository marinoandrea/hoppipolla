from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Sequence

import clingo
from policy_manager.domain.entities import (Hop, HopReading, Issuer, Path,
                                            Policy)


class HoppipollaSymbol(metaclass=ABCMeta):

    @abstractmethod
    def to_clingo(self) -> Sequence[clingo.Symbol]:
        ...


class HoppipollaMetaSymbol(HoppipollaSymbol, metaclass=ABCMeta):
    ...


class PathSymbol(HoppipollaSymbol):

    def __init__(self, path: Path) -> None:
        self.path = path

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        return [clingo.Function(
            "path",
            [clingo.String(self.path.fingerprint)]
        )]

    def __str__(self) -> str:
        return f'path("{self.path.fingerprint}").'


class HopSymbol(HoppipollaSymbol):

    def __init__(self, hop: Hop) -> None:
        self.hop = hop

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        return [clingo.Function(
            "hop",
            [clingo.String(self.hop.isd_as)]
        )]

    def __str__(self) -> str:
        return f'hop("{self.hop.isd_as}").'


class ValidSymbol(HoppipollaSymbol):

    def __init__(self, path: Path) -> None:
        self.path = path

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        return [clingo.Function(
            "valid",
            [clingo.String(self.path.fingerprint)]
        )]

    def __str__(self) -> str:
        return f'valid("{self.path.fingerprint}").'


class HopReadingSymbol(HoppipollaSymbol):

    def __init__(self, reading: HopReading) -> None:
        self.reading = reading

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        symbols: list[clingo.Symbol] = []
        symbols.append(clingo.Function(
            "data",
            [clingo.String(str(self.reading["id"]))]
        ))
        for field in self.reading:
            if field == "id":
                continue
            parsed = self._parse_value(field)
            value = clingo.Number(parsed) if type(parsed) is int\
                else clingo.String(str(parsed))
            symbols.append(clingo.Function(field, [value]))
        return symbols

    def _parse_value(self, field: str) -> int | str:
        raw_value = self.reading[field]
        if isinstance(raw_value, datetime):
            return int(raw_value.timestamp() * 1000)
        elif type(raw_value) is int:
            return raw_value
        elif type(raw_value) is float:
            return int(round(raw_value))
        else:
            return str(raw_value)

    def __str__(self) -> str:
        lines = []
        lines.append(f'data("{self.reading['id']}").')
        for field in self.reading:
            if field == "id":
                continue
            parsed = self._parse_value(field)
            value = parsed if type(parsed) is int else f'"{parsed}"'
            lines.append(f'{field}({value}).')
        return "\n".join(lines)


class ContainsSymbol(HoppipollaSymbol):

    def __init__(self, path: Path, hop: Hop) -> None:
        self.path = path
        self.hop = hop

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        return [clingo.Function(
            "contains",
            [clingo.String(self.path.fingerprint),
             clingo.String(self.hop.isd_as)]
        )]

    def __str__(self) -> str:
        return f'contains("{self.path.fingerprint}", "{self.hop.isd_as}").'


class CollectedSymbol(HoppipollaSymbol):

    def __init__(self, hop: Hop, reading: HopReading) -> None:
        self.hop = hop
        self.reading = reading

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        return [clingo.Function(
            "collected",
            [clingo.String(self.hop.isd_as),
             clingo.String(str(self.reading["id"])),]
        )]

    def __str__(self) -> str:
        return f'collected("{self.hop.isd_as}", "{self.reading['id']}").'


class PolicySymbol(HoppipollaMetaSymbol):

    def __init__(self, policy: Policy) -> None:
        self.policy = policy

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        return [
            clingo.Function(
                "policy",
                [clingo.String(str(self.policy.id))],
            ),
            clingo.Function(
                "has_issued",
                [clingo.String(str(self.policy.issuer.id)),
                 clingo.String(str(self.policy.id))],
            )
        ]

    def __str__(self) -> str:
        return "\n".join([
            f'policy("{self.policy.id}").',
            f'has_issued("{self.policy.issuer.id}", "{self.policy.id}").',
        ])


class IssuerSymbol(HoppipollaMetaSymbol):

    def __init__(self, issuer: Issuer) -> None:
        self.issuer = issuer

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        return [clingo.Function(
            "issuer",
            [clingo.String(str(self.issuer.id))]
        )]

    def __str__(self) -> str:
        return f'issuer("{self.issuer.id}").'


class OverridesSymbol(HoppipollaMetaSymbol):

    def __init__(self, policy_a: Policy, policy_b: Policy) -> None:
        self.policy_a = policy_a
        self.policy_b = policy_b

    def to_clingo(self) -> Sequence[clingo.Symbol]:
        return [clingo.Function(
            "overrides",
            [clingo.String(str(self.policy_a.id)),
             clingo.String(str(self.policy_b.id))]
        )]

    def __str__(self) -> str:
        return f'overrides("{self.policy_a.id}", "{self.policy_b.id}").'
