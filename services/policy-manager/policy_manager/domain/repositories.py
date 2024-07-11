from abc import ABCMeta, abstractmethod
from typing import Generic, Optional, TypeVar

from .entities import Entity, Identifier, Issuer, MetaPolicy, Policy

TEntity = TypeVar("TEntity", bound=Entity)


class EntityRepository(Generic[TEntity]):

    @abstractmethod
    def add(self, policy: TEntity):
        raise NotImplementedError()

    @abstractmethod
    def remove(self, policy: TEntity):
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, id: Identifier) -> Optional[TEntity]:
        raise NotImplementedError()

    def __getitem__(self, id: Identifier) -> Optional[TEntity]:
        return self.get_by_id(id)


class PolicyRepository(EntityRepository[Policy], metaclass=ABCMeta):

    @abstractmethod
    def get_all_active(self) -> list[Policy]:
        raise NotImplementedError()

    @abstractmethod
    def get_by_issuer_id(self, issuer_id: Identifier) -> list[Policy]:
        raise NotImplementedError()


class MetaPolicyRepository(EntityRepository[MetaPolicy], metaclass=ABCMeta):

    @abstractmethod
    def get_all_active(self) -> list[MetaPolicy]:
        raise NotImplementedError()


class IssuerRepository(EntityRepository[Issuer], metaclass=ABCMeta):
    ...
