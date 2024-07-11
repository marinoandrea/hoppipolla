from policy_manager.domain.entities import Issuer, MetaPolicy, Policy
from policy_manager.infra.database.vendors.sqlalchemy.models import (
    IssuerModel, MetaPolicyModel, PolicyModel)


def map_issuer_model_to_entity(model: IssuerModel) -> Issuer:
    """
    Converts a persistance layer Issuer model to a domain entity.
    """
    return Issuer(
        id=model.id,
        created_at=model.created_at,
        updated_at=model.updated_at,
        name=model.name,
    )


def map_issuer_entity_to_model(entity: Issuer) -> IssuerModel:
    """
    Converts a domain Issuer entity to a persistance layer model.
    """
    return IssuerModel(
        id=entity.id,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        name=entity.name
    )


def map_policy_model_to_entity(model: PolicyModel) -> Policy:
    """
    Converts a persistance layer Policy model to a domain entity.
    """
    return Policy(
        id=model.id,
        created_at=model.created_at,
        updated_at=model.updated_at,
        statements=model.statements,
        description=model.description,
        active=model.active,
        issuer=map_issuer_model_to_entity(model.issuer)
    )


def map_policy_entity_to_model(entity: Policy) -> PolicyModel:
    """
    Converts a domain Policy entity to a persistance layer model.
    """
    return PolicyModel(
        id=entity.id,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        statements=entity.statements,
        description=entity.description,
        active=entity.active,
        issuer=map_issuer_entity_to_model(entity.issuer)
    )


def map_meta_policy_model_to_entity(model: MetaPolicyModel) -> MetaPolicy:
    """
    Converts a persistance layer MetaPolicy model to a domain entity.
    """
    return MetaPolicy(
        id=model.id,
        created_at=model.created_at,
        updated_at=model.updated_at,
        statements=model.statements,
    )


def map_meta_policy_entity_to_model(entity: MetaPolicy) -> MetaPolicyModel:
    """
    Converts a domain MetaPolicy entity to a persistance layer model.
    """
    return MetaPolicyModel(
        id=entity.id,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        statements=entity.statements,
    )
