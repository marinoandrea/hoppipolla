from abc import ABCMeta
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from policy_manager.domain.asp import AspManager

# these identifier related assignments allow to change the ID generation logic
# across the whole domain layer for this service
Identifier = UUID
generate_identifier = uuid4


@dataclass
class Entity(metaclass=ABCMeta):
    """
    Represents an abstract entity in the domain.
    """
    id: Identifier = field(default_factory=generate_identifier)
    """Unique identifier for the entity"""

    created_at: datetime = field(default_factory=datetime.now)
    """Creation timestamp for the entity"""

    updated_at: datetime = field(default_factory=datetime.now)
    """Last modification timestamp for the entity"""

    def __post_init__(self):
        if self.created_at > self.updated_at:
            raise ValueError("created_at cannot be greater than updated_at")


@dataclass
class Issuer(Entity):
    """
    Represents a policy-maker. This is an entity representing anything from
    an individual to an organization (e.g. governmental agency, company etc.).
    """
    name: str = field(default="local")
    """Name of the issuing body or individual"""

    description: str | None = field(default=None)
    """Human-readable description of the issuer"""

    def __post_init__(self):
        super().__post_init__()
        if len(self.name) <= 1:
            raise ValueError("Issuer name must be longer than 1 character")

    def set_name(self, new_name: str) -> None:
        """
        Change the name of the issuer.
        """
        self.name = new_name
        self.updated_at = datetime.now()


@dataclass
class Policy(Entity):
    """
    Represents a policy object. It contains the string representation of the
    ASP source code as uploaded by the user before consolidation and grounding.
    """
    issuer: Issuer = field(default_factory=Issuer)
    """The entity that published the policy"""

    statements: str = field(default="")
    """ASP source code for the policy"""

    description: str | None = field(default=None)
    """Human-readable description of the policy"""

    active: bool = field(default=True)
    """
    Whether the policy is currently in use (false if overridden by a meta-rule)
    """

    def __post_init__(self):
        super().__post_init__()
        AspManager.check_syntax(self.statements, check_conflicts=True)

    def conflicts_with(self, other: Self) -> bool:
        """
        Check whether this policy conflicts with the other provided policy.
        """
        merged = "\n".join((self.statements, other.statements))
        try:
            AspManager.check_syntax(merged, check_conflicts=True)
            return False
        except ValueError:
            return True

    def deactivate(self) -> None:
        """
        Flag this policy as non-active due to a meta-constraint.
        """
        self.active = False
        self.updated_at = datetime.now()


@dataclass
class MetaPolicy(Entity):
    """
    Represents a meta-policy object. It contains the string representation of
    the ASP source code as uploaded by the user before consolidation and
    grounding.
    """
    statements: str = field(default="")
    """ASP source code for the policy"""

    def __post_init__(self):
        super().__post_init__()
        AspManager.check_syntax(self.statements, check_conflicts=True)


HopReading = dict[str, str | int | float]
"""
Represents an NIP data reading for a specific hop.

NOTE: as the structure might change and TypedDict does not support extra keys
as of Python 3.12 (see
https://discuss.python.org/t/pep-728-typeddict-with-typed-extra-items/45443/102),
we allow for a slightly unsafe type.
"""


@dataclass(frozen=True)
class TimeInterval:
    datetime_start: datetime
    datetime_end: datetime


@dataclass(frozen=True)
class Hop:
    isd_as: str
    """
    SCION isolation domain + AS address.
    """

    ifid: str | None
    """
    The inbound interface identifier for the hop.
    """


@dataclass(frozen=True)
class Path:
    fingerprint: str
    """
    Unique path fingerprint.
    """

    isd_as_src: str
    """
    Path source address.
    """

    isd_as_dst: str
    """
    Path destination address.
    """

    hops: list[Hop]
    """
    List of network hops to get from source to destination.
    """
