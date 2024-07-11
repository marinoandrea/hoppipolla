from abc import ABCMeta, abstractmethod
from typing import Callable, Generic, Literal, Optional, TypeVar, cast

from policy_manager.domain.entities import (Entity, Identifier, Issuer,
                                            MetaPolicy, Policy)
from policy_manager.domain.repositories import (EntityRepository,
                                                IssuerRepository,
                                                MetaPolicyRepository,
                                                PolicyRepository)
from sqlalchemy.orm import Query, Session

from .models import BaseModel, IssuerModel, MetaPolicyModel, PolicyModel
from .utils import (map_issuer_entity_to_model, map_issuer_model_to_entity,
                    map_meta_policy_entity_to_model,
                    map_meta_policy_model_to_entity,
                    map_policy_entity_to_model, map_policy_model_to_entity)

RemovedPlaceholder = Literal["REMOVED"]
REMOVED: RemovedPlaceholder = "REMOVED"


TEntity = TypeVar("TEntity", bound=Entity)
TModel = TypeVar("TModel", bound=BaseModel)


class SQLAlchemyRepository(
    Generic[TModel, TEntity],
    EntityRepository[TEntity],
    metaclass=ABCMeta
):
    def __init__(
        self,
        map_entity_to_model: Callable[[TEntity], TModel],
        map_model_to_entity: Callable[[TModel], TEntity],
        session: Session,
        identity_map: dict[
            Identifier, Optional[TEntity] | RemovedPlaceholder] | None = None
    ) -> None:
        self.session = session
        self.map_entity_to_model = map_entity_to_model
        self.map_model_to_entity = map_model_to_entity
        self._identity_map = {} if identity_map is None else identity_map

    @abstractmethod
    def get_query(self) -> Query[TModel]:
        raise NotImplementedError()

    def add(self, entity: TEntity):
        self._identity_map[entity.id] = entity
        model = self.map_entity_to_model(entity)
        self.session.add(model)

    def remove(self, entity: TEntity):
        self._assert_not_removed(entity)
        self._identity_map[entity.id] = REMOVED
        model = self.get_query().get(entity.id)
        self.session.delete(model)

    def get_by_id(self, id: Identifier) -> Optional[TEntity]:
        model = self.get_query().get(id)
        if model is None:
            return None
        # casting here is safe, sqlalchemy returns Any
        return self._get_entity(cast(TModel, model))

    def _assert_not_removed(self, entity: TEntity):
        result = self._identity_map.get(entity.id, None)
        assert result != REMOVED, f"Entity {entity.id} already removed"

    def _get_entity(self, model: TModel) -> TEntity:
        entity = self.map_model_to_entity(model)

        self._assert_not_removed(entity)

        if entity.id in self._identity_map:
            # casting here is safe as we already checked for removal
            return cast(TEntity, self._identity_map[entity.id])

        self._identity_map[entity.id] = entity
        return entity

    def persist(self, entity: TEntity):
        self._assert_not_removed(entity)

        # sanity check
        assert entity.id in self._identity_map, \
            f"Entity {entity.id} not previously added to identity map"

        model = self.map_entity_to_model(entity)

        merged = self.session.merge(model)
        self.session.add(merged)

    def persist_all(self):
        for entity in self._identity_map.values():
            if entity is not None and entity != REMOVED:
                self.persist(entity)


class SQLAlchemyPolicyRepository(
    PolicyRepository,
    SQLAlchemyRepository[PolicyModel, Policy]
):
    session: Session
    _identity_map: dict[Identifier, Optional[Policy] | RemovedPlaceholder]

    def __init__(
        self,
        session: Session,
        identity_map: dict[
            Identifier, Optional[Policy] | RemovedPlaceholder] = {}
    ) -> None:
        super().__init__(
            map_policy_entity_to_model,
            map_policy_model_to_entity,
            session,
            identity_map
        )

    def get_query(self) -> Query[PolicyModel]:
        return self.session.query(PolicyModel)

    def get_by_issuer_id(self, issuer_id: Identifier) -> list[Policy]:
        results = self.get_query()\
            .filter_by(issuer_id=issuer_id)\
            .all()
        return [self._get_entity(model) for model in results]

    def get_all_active(self) -> list[Policy]:
        results = self.get_query()\
            .filter_by(active=True)\
            .all()
        return [self._get_entity(model) for model in results]


class SQLAlchemyIssuerRepository(
    IssuerRepository,
    SQLAlchemyRepository[IssuerModel, Issuer]
):
    session: Session
    _identity_map: dict[Identifier, Optional[Issuer] | RemovedPlaceholder]

    def __init__(
        self,
        session: Session,
        identity_map: dict[
            Identifier, Optional[Issuer] | RemovedPlaceholder] = {}
    ) -> None:
        super().__init__(
            map_issuer_entity_to_model,
            map_issuer_model_to_entity,
            session,
            identity_map
        )

    def get_query(self) -> Query[IssuerModel]:
        return self.session.query(IssuerModel)


class SQLAlchemyMetaPolicyRepository(
    MetaPolicyRepository,
    SQLAlchemyRepository[MetaPolicyModel, MetaPolicy]
):
    session: Session
    _identity_map: dict[Identifier, Optional[MetaPolicy] | RemovedPlaceholder]

    def __init__(
        self,
        session: Session,
        identity_map: dict[
            Identifier, Optional[MetaPolicy] | RemovedPlaceholder] = {}
    ) -> None:
        super().__init__(
            map_meta_policy_entity_to_model,
            map_meta_policy_model_to_entity,
            session,
            identity_map
        )

    def get_query(self) -> Query[MetaPolicyModel]:
        return self.session.query(MetaPolicyModel)

    def get_all_active(self) -> list[MetaPolicy]:
        results = self.get_query().all()
        return [self._get_entity(model) for model in results]
