from datetime import datetime

import clingo
from policy_manager.entities import Path, Policy

from .grammar import (CollectedSymbol, ContainsSymbol, DataSymbol,
                      HoppipollaSymbol, HopSymbol, PathSymbol)

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


class AspManager:
    counter: int = 0
    updated_at: datetime = datetime.now()
    _policies: list[Policy] = []

    def _validate_policy(self, statements: str) -> None:
        try:
            ctl = clingo.Control()
            ctl.add("base", [], statements)
            ctl.ground([("base", [])])
        except RuntimeError as e:
            raise ValueError(str(e))

    def _instantiate_path(self, path: Path) -> str:
        out: list[HoppipollaSymbol] = [PathSymbol(path)]
        for hop in path.hops:
            out.append(HopSymbol(hop))
            out.append(ContainsSymbol(path, hop))
            for data in hop.collected_data:
                out.append(DataSymbol(data))
                out.append(CollectedSymbol(hop, data))
        return "\n\n".join(map(repr, out))

    @property
    def policies(self) -> list[Policy]:
        return self._policies

    @policies.setter
    def policies(self, policies: list[Policy]) -> None:
        self._policies = policies
        self.updated_at = datetime.now()

    def create_policy(self, statements: str) -> Policy:
        """
        Validate and conditionally add a policy to the ASP manager.

        Parameters
        ---
        statements `str`
            The policy ASP source code

        Raises
        ---
        `ValueError`
            If the policy is not syntactically correct.

        Returns
        ---
        Policy dataclass with identifier
        """
        self._validate_policy(statements)

        self.counter += 1
        policy = Policy(self.counter, statements)
        self.policies.append(policy)

        return policy

    def remove_policy(self, policy_id: int) -> None:
        """
        Remove a policy from the ASP manager.

        Parameters
        ---
        policy_id `int`
            The ID of the policy to be removed
        """
        self.policies = list(
            filter(lambda x: x.id == policy_id, self.policies))

    def update_policy(self, policy_id: int, statements: str) -> Policy:
        """
        Validate and conditionally add a policy to the ASP manager.

        Parameters
        ---
        policy_id `int`
            The ID of the policy to be updated
        statements `str`
            The policy ASP source code

        Raises
        ---
        `ValueError`
            If the policy is not syntactically correct or the id is not found.

        Returns
        ---
        Policy dataclass with identifier
        """
        self._validate_policy(statements)

        policies = [*self._policies]
        policy = Policy(policy_id, statements)

        idx = -1
        for i in range(len(self.policies)):
            if self.policies[i].id != policy_id:
                continue
            idx = i
            break

        if idx == -1:
            raise ValueError(f"{policy_id=} does not exist")

        policies[idx] = policy
        self.policies = [*policies]

        return policy

    def validate(self, path: Path) -> bool:
        """
        Check whether a given SCION path complies with the published policies.

        Parameters
        ---
        path `Path`
            The path to validate

        Returns
        ---
        True or false
        """
        program: str = PRELUDE
        for policy in self.policies:
            program += f"\n{policy.statements}"
        program += f"\n{self._instantiate_path(path)}"

        ctl = clingo.Control()
        ctl.add("base", [], program)
        ctl.ground()

        res = ctl.solve()

        return bool(res.satisfiable)
