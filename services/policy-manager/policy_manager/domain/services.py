from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Iterator

from .entities import Hop, HopReading, MetaPolicy, Path, Policy, TimeInterval


class NipProxy(metaclass=ABCMeta):
    """
    Service that exposes an API to retrieve Network Information Plane (NIP)
    data readings about hops in the network.
    """

    @abstractmethod
    def get_readings_for_interval(
            self,
            interval: TimeInterval,
            hop: Hop
    ) -> list[HopReading]:
        """
        Fetch data readings collected in the time interval for the provided hop.

        Parameters
        ----------
        interval: `TimeInterval`
            Timestamp window to filter the data readings based on their
            collection time
        hop: `Hop`
            Network hop to fetch readings for

        Raises
        ------
        `ExternalServiceError`
            If the external NIP client is not reachable or returns an error

        Returns
        -------
        `list[HopReading]`
            A collection of data readings for the hop filtered by time interval
        """
        ...


class ConflictResolutionStatus(Enum):
    RESOLVED = "RESOLVED"
    NOT_RESOLVED = "NOT_RESOLVED"


@dataclass(frozen=True)
class ConflictResolutionResult:
    """
    Result of a meta-policy conflict resolution action.
    """
    status: ConflictResolutionStatus = ConflictResolutionStatus.NOT_RESOLVED
    """
    The status of the conflict, whether it can be resolved or not.
    """

    policy_weak: Policy | None = None
    """
    The policy that is overridden.
    """

    policy_strong: Policy | None = None
    """
    The policy that overriddes.
    """

    def __post_init__(self):
        if self.status == ConflictResolutionStatus.NOT_RESOLVED:
            assert self.policy_strong is None\
                and self.policy_weak is None
        else:
            assert self.policy_strong is not None\
                and self.policy_weak is not None


class AspMetaHandle(metaclass=ABCMeta):
    """
    Utility to perform conflict resolution based on meta-policies.
    """

    @abstractmethod
    def resolve_conflicts(
        self,
        p1: Policy,
        p2: Policy
    ) -> ConflictResolutionResult:
        """
        Perform a conflict resolution action based on meta-policies
        """
        ...


class AspManager(metaclass=ABCMeta):
    """
    Service that offers ASP-related functionalities for the domain.
    """

    @abstractmethod
    def check_syntax(self, statements: str) -> None:
        """
        Check whether the ASP syntax for the provided statements is valid.

        Parameters
        ----------
        statements: `str`
            The ASP source code to check

        Raises
        ------
        `ValueError`
            If the policy has syntax errors or internal conflicts
        """
        ...

    @contextmanager
    @abstractmethod
    def meta(self, meta_policies: list[MetaPolicy]) -> Iterator[AspMetaHandle]:
        """
        Yield a context manager that allows to handle meta-policy logic.

        Parameters
        ----------
        meta_policies: `list[MetaPolicy]`
            The published meta-policies to initialize the handle with

        Returns
        -------
        `Iterator[AspMetaHandle]`
            A yielded instance of `AspMetaHandle` initialized with the
            provided meta-policies.
        """
        ...

    @abstractmethod
    def validate(
        self,
        policy: Policy,
        path: Path,
        readings: list[HopReading]
    ) -> bool:
        """
        Check whether a given SCION path complies with the provided policy.

        Parameters
        ----------
        policy: `Policy`
            The policy to use for path validation
        path: `Path`
            The SCION path representation to validate
        readings: `list[HopReading]`
            The NIP data readings for the hops contained in the path

        Returns
        -------
        `bool`
            Whether the path is valid or not given the provided policy
        """
        ...
