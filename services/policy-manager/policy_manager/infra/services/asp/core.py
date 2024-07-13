import os
from abc import ABCMeta
from contextlib import contextmanager
from functools import lru_cache
from typing import Iterator, Self, Sequence

import clingo
from policy_manager.domain.entities import HopReading, MetaPolicy, Path, Policy
from policy_manager.domain.services import (AspManager, AspMetaHandle,
                                            ConflictResolutionResult,
                                            ConflictResolutionStatus)

from .grammar import (CollectedSymbol, ContainsSymbol, HoppipollaSymbol,
                      HopReadingSymbol, HopSymbol, IssuerSymbol,
                      OverridesSymbol, PathSymbol, PolicySymbol, ValidSymbol)

PATH_PRELUDE = os.path.join(os.path.dirname(__file__), "lps", "prelude.lp")
PATH_PRELUDE_META = os.path.join(os.path.dirname(__file__), "lps", "prelude-meta.lp")


@lru_cache
def load_prelude():
    with open(PATH_PRELUDE) as f:
        return f.read()


@lru_cache
def load_prelude_meta():
    with open(PATH_PRELUDE_META) as f:
        return f.read()


class HoppipollaClingoProgram(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.control = clingo.Control()
        self._string = ""

    def add(self, symbol: HoppipollaSymbol) -> Self:
        self._string += f"\n{str(symbol)}"
        with self.control.backend() as backend:
            for clingo_symbol in symbol.to_clingo():
                atom = backend.add_atom(clingo_symbol)
                backend.add_rule([atom])
        return self

    def __str__(self) -> str:
        return self._string


class HoppipollaClingoPolicyProgram(HoppipollaClingoProgram):
    def __init__(self, policy: Policy) -> None:
        super().__init__()
        prelude = load_prelude()
        self._string += prelude
        self.control.add("base", [], prelude)
        try:
            self._string += policy.statements
            self.control.add("base", [], policy.statements)
        except (RuntimeError, MemoryError) as e:
            raise ValueError(e)

    def validate(
        self,
        path: Path,
        readings: Sequence[HopReading]
    ) -> bool:
        self.add(PathSymbol(path))
        for hop in path.hops:
            self.add(HopSymbol(hop))
            self.add(ContainsSymbol(path, hop))
            for reading in filter(lambda r: r["isd_as"] == hop.isd_as, readings):
                self.add(HopReadingSymbol(reading))
                self.add(CollectedSymbol(hop, reading))
        self.add(ValidSymbol(path))
        self.control.ground()
        result = self.control.solve()
        return bool(result.satisfiable)


class HoppipollaClingoMetaPolicyProgram(HoppipollaClingoProgram, AspMetaHandle):
    def __init__(self, meta_policies: list[MetaPolicy]) -> None:
        super().__init__()
        self.meta_policies = meta_policies
        prelude = load_prelude_meta()
        self._string += prelude
        self.control.add("base", [], prelude)
        try:
            for meta_policy in self.meta_policies:
                self._string += meta_policy.statements
                self.control.add("base", [], meta_policy.statements)
        except (RuntimeError, MemoryError) as e:
            raise ValueError(e)

    def resolve_conflicts(self, policy_a: Policy, policy_b: Policy) -> ConflictResolutionResult:
        self.add(IssuerSymbol(policy_a.issuer))\
            .add(IssuerSymbol(policy_b.issuer))\
            .add(PolicySymbol(policy_a))\
            .add(PolicySymbol(policy_b))

        self.control.ground()

        pred_a_ovverides_b = OverridesSymbol(policy_a, policy_b).to_clingo()[0]
        pred_b_overrides_a = OverridesSymbol(policy_b, policy_a).to_clingo()[0]
        with self.control.solve(yield_=True) as handle:
            for model in handle:
                a_overrides_b = model.contains(pred_a_ovverides_b)
                b_overrides_a = model.contains(pred_b_overrides_a)

                if a_overrides_b and not b_overrides_a:
                    return ConflictResolutionResult(
                        status=ConflictResolutionStatus.RESOLVED,
                        policy_strong=policy_a,
                        policy_weak=policy_b
                    )
                elif b_overrides_a and not a_overrides_b:
                    return ConflictResolutionResult(
                        status=ConflictResolutionStatus.RESOLVED,
                        policy_strong=policy_b,
                        policy_weak=policy_a
                    )
                # the issuers have equal power
                elif a_overrides_b and b_overrides_a:
                    policy_latest = policy_a if policy_a.created_at > policy_b.created_at else policy_b
                    policy_oldest = policy_a if policy_a.created_at < policy_b.created_at else policy_b
                    return ConflictResolutionResult(
                        status=ConflictResolutionStatus.RESOLVED,
                        policy_strong=policy_latest,
                        policy_weak=policy_oldest
                    )

        # the power cannot be determined
        return ConflictResolutionResult(
            status=ConflictResolutionStatus.NOT_RESOLVED)


class ClingoAspManager(AspManager):

    def check_syntax(self, statements: str, check_conflicts=False) -> None:
        try:
            ctl = clingo.Control(message_limit=0)
            ctl.add("base", [], statements)
            ctl.ground()
            if check_conflicts and ctl.is_conflicting:
                raise ValueError("Policy has internal conflicts")
        except RuntimeError as e:
            raise ValueError(str(e))

    @contextmanager
    def meta(self, meta_policies: list[MetaPolicy]) -> Iterator[HoppipollaClingoMetaPolicyProgram]:
        yield HoppipollaClingoMetaPolicyProgram(meta_policies)

    def validate(
        self,
        policy: Policy,
        path: Path,
        readings: list[HopReading]
    ) -> bool:
        return HoppipollaClingoPolicyProgram(policy).validate(path, readings)
