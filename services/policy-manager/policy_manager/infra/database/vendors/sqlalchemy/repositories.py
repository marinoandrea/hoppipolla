from abc import ABCMeta, abstractmethod
from datetime import datetime
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
        session: Session,
        map_entity_to_model: Callable[[TEntity], TModel],
        map_model_to_entity: Callable[[TModel], TEntity],
    ) -> None:
        self.session = session
        self.map_entity_to_model = map_entity_to_model
        self.map_model_to_entity = map_model_to_entity

    @abstractmethod
    def get_query(self) -> Query[TModel]:
        ...

    def add(self, entity: TEntity):
        model = self.map_entity_to_model(entity)
        self.session.merge(model)

    def remove(self, id: Identifier):
        model = self.get_query().get(id)
        self.session.delete(model)

    def get_by_id(self, id: Identifier) -> Optional[TEntity]:
        model = self.get_query().get(id)
        if model is None:
            return None
        # casting here is safe, sqlalchemy returns Any
        return self.map_model_to_entity(cast(TModel, model))


class SQLAlchemyPolicyRepository(
    PolicyRepository,
    SQLAlchemyRepository[PolicyModel, Policy]
):
    def __init__(self, session: Session) -> None:
        super().__init__(
            session,
            map_policy_entity_to_model,
            map_policy_model_to_entity
        )

    def get_query(self) -> Query[PolicyModel]:
        return self.session.query(PolicyModel)

    def get_by_issuer_id(self, issuer_id: Identifier) -> list[Policy]:
        results = self.get_query()\
            .filter_by(issuer_id=issuer_id)\
            .all()
        return [self.map_model_to_entity(model) for model in results]

    def get_all_active(self) -> list[Policy]:
        results = self.get_query()\
            .filter_by(active=True)\
            .all()
        return [self.map_model_to_entity(model) for model in results]

    def get_max_created_at(self) -> datetime:
        result = self.get_query()\
            .filter_by(active=True)\
            .order_by(PolicyModel.created_at.desc())\
            .first()
        return result.created_at if result is not None else datetime.now()


class SQLAlchemyIssuerRepository(
    IssuerRepository,
    SQLAlchemyRepository[IssuerModel, Issuer]
):
    def __init__(self, session: Session) -> None:
        super().__init__(
            session,
            map_issuer_entity_to_model,
            map_issuer_model_to_entity
        )

    def get_query(self) -> Query[IssuerModel]:
        return self.session.query(IssuerModel)

    def get_one_default(self) -> Issuer | None:
        model = self.session.query(IssuerModel)\
            .filter_by(default=True)\
            .first()
        return self.map_model_to_entity(model) if model is not None else None


class SQLAlchemyMetaPolicyRepository(
    MetaPolicyRepository,
    SQLAlchemyRepository[MetaPolicyModel, MetaPolicy]
):
    def __init__(self, session: Session) -> None:
        super().__init__(
            session,
            map_meta_policy_entity_to_model,
            map_meta_policy_model_to_entity
        )

    def get_query(self) -> Query[MetaPolicyModel]:
        return self.session.query(MetaPolicyModel)

    def get_all_active(self) -> list[MetaPolicy]:
        results = self.get_query().all()
        return [self.map_model_to_entity(model) for model in results]

    def get_max_created_at(self) -> datetime:
        result = self.get_query()\
            .order_by(MetaPolicyModel.created_at.desc())\
            .first()
        return result.created_at if result is not None else datetime.now()
