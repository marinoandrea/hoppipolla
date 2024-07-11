from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import partial
from multiprocessing.pool import ThreadPool
from typing import cast

from policy_manager.domain.asp import AspManager, ConflictResolutionStatus
from policy_manager.domain.entities import (HopReading, Identifier, Path,
                                            Policy, TimeInterval)
from policy_manager.domain.errors import (ExternalServiceError,
                                          InvalidInputError)
from policy_manager.domain.repositories import (IssuerRepository,
                                                MetaPolicyRepository,
                                                PolicyRepository)
from policy_manager.domain.services import NipClientService


@dataclass(frozen=True)
class CreatePolicyInput:
    issuer_id: Identifier
    statements: str
    description: str | None


@dataclass(frozen=True)
class CreatePolicyOutput:
    policy: Policy


def create_policy(
    policy_repository: PolicyRepository,
    issuer_repository: IssuerRepository,
    meta_policy_repository: MetaPolicyRepository,
    data: CreatePolicyInput
) -> CreatePolicyOutput:
    """
    Add a path-level policy to the service. This use-case also takes care of
    resolving conflicts and consolidating the current state of the system into
    a single policy that is then stored for later use in validation.
    """
    issuer = issuer_repository.get_by_id(data.issuer_id)

    if issuer is None:
        raise InvalidInputError(
            "issuer_id", data.issuer_id, "Issuer does not exist")

    try:
        new_policy = Policy(
            issuer=issuer,
            statements=data.statements,
            description=data.description
        )
    except ValueError:
        raise InvalidInputError(
            "statements", data.statements, "Invalid ASP syntax for policy")

    policy_repository.add(new_policy)

    for old_policy in policy_repository.get_all_active():
        if not new_policy.conflicts_with(old_policy):
            continue

        # this is cached per session so it's fine to call it at every iteration
        meta_policies = meta_policy_repository.get_all_active()

        result = AspManager.resolve_conflicts(
            meta_policies,
            new_policy,
            old_policy
        )

        if result.status == ConflictResolutionStatus.NOT_RESOLVED:
            policy_repository.remove(new_policy)
            raise InvalidInputError(
                "statements",
                data.statements,
                f"Conflict with {old_policy} cannot be resolved"
            )

        # cast is safe due to validation logic of result
        cast(Policy, result.policy_weak).deactivate()

    return CreatePolicyOutput(policy=new_policy)


def generate_validation_default_interval():
    datetime_end = datetime.now()
    datetime_start = datetime_end - timedelta(days=7)
    return TimeInterval(datetime_start, datetime_end)


@dataclass(frozen=True)
class ValidatePathInput:
    path: Path
    interval: TimeInterval = field(
        default_factory=generate_validation_default_interval)


@dataclass(frozen=True)
class ValidatePathOutput:
    valid: bool


def validate_path(
    policy_repository: PolicyRepository,
    nip_client_service: NipClientService,
    input_data: ValidatePathInput
) -> ValidatePathOutput:
    """
    Check whether a provided path is valid given the active policies.
    """
    active_policies = policy_repository.get_all_active()

    try:
        readings: list[HopReading] = []
        with ThreadPool(processes=len(input_data.path.hops)) as pool:
            results = pool.map(
                partial(
                    nip_client_service.get_readings_for_interval,
                    input_data.interval
                ),
                input_data.path.hops
            )
            for result in results:
                readings.extend(result)

    except Exception as e:
        raise ExternalServiceError("NipClientService", str(e))

    valid = AspManager.validate(active_policies, input_data.path, readings)

    return ValidatePathOutput(valid=valid)