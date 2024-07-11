import clingo
from policy_manager.domain.entities import HopReading, MetaPolicy, Path, Policy
from policy_manager.domain.services import (AspManager,
                                            ConflictResolutionResult,
                                            ConflictResolutionStatus)

from .grammar import (CollectedSymbol, ContainsSymbol, HopReadingSymbol,
                      HopSymbol, IssuerSymbol, OverpowersSymbol, PathSymbol,
                      PolicySymbol)

PRELUDE = '''
% basic types
hop(Hop)    :- contains(Path, Hop), path(Path).
path(Path)  :- contains(Path, Hop), hop(Hop).
data(Data)  :- collected(Hop, Data), hop(Hop).
hop(Hop)    :- collected(Hop, Data), data(Data).

% sanity check for typization
:- hop(X), data(X).
:- hop(X), path(X).
:- data(X), path(X).

% utilities
latest_data_collected_date(Hop, MaxTmp) :-
    hop(Hop),
    MaxTmp = #max {
        Tmp : data_collected_date(Data, Tmp), collected(Hop, Data) }.

latest_data(Hop, Data) :-
    latest_data_collected_date(Hop, MaxTmp),
    data_collected_date(Data, MaxTmp).
'''

PRELUDE_META = '''
% type safety
:- policy(X), issuer(X).
:- has_issued(I1, P), has_issued(I2, P), issuer(I1), issuer(I2), policy(P).

% inference
issuer(I) :- has_issued(I, _).
policy(P) :- has_issued(_, P).

% definitions
overpowers(P1, P2) :-
    has_issued(I1, P1),
    has_issued(I2, P2),
    has_power_over(I1, I2).
'''


class ClingoAspManager(AspManager):

    def check_syntax(self, statements: str, check_conflicts=False) -> None:
        try:
            ctl = clingo.Control()
            ctl.add("base", [], statements)
            ctl.ground([("base", [])])
            if check_conflicts and ctl.is_conflicting:
                raise ValueError("Policy has conflicts")
        except RuntimeError as e:
            raise ValueError(str(e))

    def has_conflicts(self, p1: Policy, p2: Policy) -> bool:
        try:
            ctl = clingo.Control()
            ctl.add("base", [], p1.statements)
            ctl.add("base", [], p2.statements)
            ctl.ground([("base", [])])
            if ctl.is_conflicting:
                return True
        except RuntimeError:
            return True
        return False

    def resolve_conflicts(
        self,
        meta_policies: list[MetaPolicy],
        p1: Policy,
        p2: Policy
    ) -> ConflictResolutionResult:
        control = clingo.Control()
        control.add("base", [], PRELUDE_META)
        for mp in meta_policies:
            control.add("base", [], mp.statements)
        control.add("base", [], repr(IssuerSymbol(p1.issuer)))
        control.add("base", [], repr(IssuerSymbol(p2.issuer)))
        control.add("base", [], repr(PolicySymbol(p1)))
        control.add("base", [], repr(PolicySymbol(p2)))
        control.ground([("base", [])])

        predicate_p1p2 = repr(OverpowersSymbol(p1, p2))
        predicate_p2p1 = repr(OverpowersSymbol(p2, p1))

        with control.solve(yield_=True) as handle:
            for model in handle:
                atoms = model.symbols(atoms=True)
                p1_overpowers_p2 = any(a.match(predicate_p1p2, 2)
                                       for a in atoms)
                p2_overpowers_p1 = any(a.match(predicate_p2p1, 2)
                                       for a in atoms)

                if p1_overpowers_p2 and not p2_overpowers_p1:
                    return ConflictResolutionResult(
                        status=ConflictResolutionStatus.RESOLVED,
                        policy_strong=p1,
                        policy_weak=p2
                    )
                elif p2_overpowers_p1 and not p1_overpowers_p2:
                    return ConflictResolutionResult(
                        status=ConflictResolutionStatus.RESOLVED,
                        policy_strong=p2,
                        policy_weak=p1
                    )
                # the issuers have equal power
                elif p1_overpowers_p2 and p2_overpowers_p1:
                    policy_latest = p1 if p1.created_at > p2.created_at else p2
                    policy_oldest = p1 if p1.created_at < p2.created_at else p2
                    return ConflictResolutionResult(
                        status=ConflictResolutionStatus.RESOLVED,
                        policy_strong=policy_latest,
                        policy_weak=policy_oldest
                    )

        # the power cannot be determined
        return ConflictResolutionResult(
            status=ConflictResolutionStatus.NOT_RESOLVED)

    def validate(
        self,
        policies: list[Policy],
        path: Path,
        readings: list[HopReading]
    ) -> bool:
        """
        Check whether a given SCION path complies with the published policies.
        """
        control = clingo.Control()
        control.add("base", [], PRELUDE)

        # merge the previously validated active policies
        for p in policies:
            control.add("base", [], p.statements)

        # instantiate the path predicates
        control.add("base", [], repr(PathSymbol(path)))
        for hop in path.hops:
            control.add("base", [], repr(HopSymbol(hop)))
            control.add("base", [], repr(ContainsSymbol(path, hop)))

            hop_readings = filter(
                lambda r: r["isd_as"] == hop.isd_as, readings)

            for reading in hop_readings:
                control.add("base", [], repr(HopReadingSymbol(reading)))
                control.add("base", [], repr(CollectedSymbol(hop, reading)))

        control.ground([("base", [])])

        res = control.solve()
        return bool(res.satisfiable)
