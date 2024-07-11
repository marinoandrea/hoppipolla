import pickle
from abc import ABCMeta
from pathlib import Path
from typing import Generic, Literal, Optional, TypeVar, cast

from policy_manager.domain.entities import (Entity, Identifier, Issuer,
                                            MetaPolicy, Policy)
from policy_manager.domain.repositories import (EntityRepository,
                                                IssuerRepository,
                                                MetaPolicyRepository,
                                                PolicyRepository)

RemovedPlaceholder = Literal["REMOVED"]
REMOVED: RemovedPlaceholder = "REMOVED"


TEntity = TypeVar("TEntity", bound=Entity)


class InMemoryRepository(
    Generic[TEntity],
    EntityRepository[TEntity],
    metaclass=ABCMeta
):
    pickle_path: Path | None
    store: dict[Identifier, Optional[TEntity] | RemovedPlaceholder]

    def __init__(
        self,
        picke_path: Path | None = None,
        store: dict[Identifier, Optional[TEntity] | RemovedPlaceholder] = {}
    ) -> None:
        self.pickle_path = picke_path
        if picke_path:
            with open(picke_path, "rb") as f:
                self.store = pickle.load(f)
        else:
            self.store = store

    def add(self, entity: TEntity):
        self.store[entity.id] = entity

    def remove(self, entity: TEntity):
        self._assert_not_removed(entity)
        self.store[entity.id] = REMOVED

    def get_by_id(self, id: Identifier) -> Optional[TEntity]:
        entity = self.store[id]
        assert entity != REMOVED, f"Entity {id} already removed"
        return entity

    def _assert_not_removed(self, entity: TEntity):
        result = self.store.get(entity.id, None)
        assert result != REMOVED, f"Entity {entity.id} already removed"

    def persist(self, _entity: TEntity):
        pass

    def persist_all(self):
        for entity in self.store.values():
            if entity is not None and entity != REMOVED:
                self.persist(entity)


class SQLAlchemyPolicyRepository(
    PolicyRepository,
    InMemoryRepository[Policy]
):
    def get_by_issuer_id(self, issuer_id: Identifier) -> list[Policy]:
        out: list[Policy] = []
        for stored in self.store.values():
            if stored == REMOVED:
                continue
            policy = cast(Policy, stored)
            if policy.issuer.id != issuer_id:
                continue
            out.append(policy)
        return out

    def get_all_active(self) -> list[Policy]:
        out: list[Policy] = []
        for stored in self.store.values():
            if stored == REMOVED:
                continue
            policy = cast(Policy, stored)
            if not policy.active:
                continue
            out.append(policy)
        return out


class SQLAlchemyIssuerRepository(
    IssuerRepository,
    InMemoryRepository[Issuer]
):
    pass


class SQLAlchemyMetaPolicyRepository(
    MetaPolicyRepository,
    InMemoryRepository[MetaPolicy]
):
    def get_all_active(self) -> list[MetaPolicy]:
        out: list[MetaPolicy] = []
        for stored in self.store.values():
            if stored == REMOVED:
                continue
            policy = cast(MetaPolicy, stored)
            out.append(policy)
        return out
