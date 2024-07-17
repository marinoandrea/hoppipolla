from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Generic, Optional, TypeVar

from .entities import Entity, Identifier, Issuer, MetaPolicy, Policy

TEntity = TypeVar("TEntity", bound=Entity)


class EntityRepository(Generic[TEntity]):
    """
    Abstract interface for an implementation of the repository pattern for a
    specific entity.
    """

    @abstractmethod
    def add(self, policy: TEntity):
        """
        Add a new entity to the repository or modify the entity with the same
        identifier.
        """
        ...

    @abstractmethod
    def remove(self, policy: TEntity):
        """
        Remove an entity from the repository.
        """
        ...

    @abstractmethod
    def get_by_id(self, id: Identifier) -> Optional[TEntity]:
        """
        Fetch an entity by its identifier.
        """
        ...

    def __getitem__(self, id: Identifier) -> Optional[TEntity]:
        return self.get_by_id(id)


class PolicyRepository(EntityRepository[Policy], metaclass=ABCMeta):
    """
    Implementation of the repository pattern for the `Policy` entity.
    """

    @abstractmethod
    def get_all_active(self) -> list[Policy]:
        """
        Fetch all policies that have been published and flagged as active.
        """
        ...

    @abstractmethod
    def get_by_issuer_id(self, issuer_id: Identifier) -> list[Policy]:
        """
        Fetch all policies with the provided issuer identifier.
        """
        ...

    @abstractmethod
    def get_max_created_at(self) -> datetime:
        """
        Fetch the latest policy creation timestamp.
        """
        ...


class MetaPolicyRepository(EntityRepository[MetaPolicy], metaclass=ABCMeta):
    """
    Implementation of the repository pattern for the `MetaPolicy` entity.
    """

    @abstractmethod
    def get_all_active(self) -> list[MetaPolicy]:
        """
        Fetch all meta-policies that have been published and flagged as active.
        """
        ...

    @abstractmethod
    def get_max_created_at(self) -> datetime:
        """
        Fetch the latest policy creation timestamp.
        """
        ...


class IssuerRepository(EntityRepository[Issuer], metaclass=ABCMeta):
    """
    Implementation of the repository pattern for the `Issuer` entity.
    """

    @abstractmethod
    def get_one_default(self) -> Issuer | None:
        """
        Fetch a default issuer for the application instance.
        """
        ...
