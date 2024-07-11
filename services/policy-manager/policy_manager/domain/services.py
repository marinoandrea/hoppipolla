from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .entities import Hop, HopReading, MetaPolicy, Path, Policy, TimeInterval


class NipClientService(metaclass=ABCMeta):

    @abstractmethod
    def get_readings_for_interval(
            self, interval: TimeInterval, hop: Hop) -> list[HopReading]:
        ...


class ConflictResolutionStatus(Enum):
    RESOLVED = "RESOLVED"
    NOT_RESOLVED = "NOT_RESOLVED"


@dataclass(frozen=True)
class ConflictResolutionResult:
    status: ConflictResolutionStatus = ConflictResolutionStatus.NOT_RESOLVED
    policy_weak: Policy | None = None
    policy_strong: Policy | None = None

    def __post_init__(self):
        if self.status == ConflictResolutionStatus.NOT_RESOLVED:
            assert self.policy_strong is None\
                and self.policy_weak is None
        else:
            assert self.policy_strong is not None\
                and self.policy_weak is not None


class AspManager(metaclass=ABCMeta):

    @abstractmethod
    def check_syntax(self, statements: str, check_conflicts=False) -> None:
        ...

    @abstractmethod
    def has_conflicts(self, p1: Policy, p2: Policy) -> bool:
        ...

    @abstractmethod
    def resolve_conflicts(
        self,
        meta_policies: list[MetaPolicy],
        p1: Policy,
        p2: Policy
    ) -> ConflictResolutionResult:
        ...

    @abstractmethod
    def validate(
        self,
        policies: list[Policy],
        path: Path,
        readings: list[HopReading]
    ) -> bool:
        ...
