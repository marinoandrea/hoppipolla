import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from functools import partial
from multiprocessing.pool import ThreadPool
from typing import Optional

from policy_manager.domain.entities import (HopReading, Identifier, Issuer,
                                            Path, Policy, TimeInterval)
from policy_manager.domain.errors import (ExternalServiceError,
                                          InvalidInputError)
from policy_manager.domain.repositories import (IssuerRepository,
                                                MetaPolicyRepository,
                                                PolicyRepository)

from .services import AspManager, ConflictResolutionStatus, NipProxy


@dataclass(frozen=True)
class CreatePolicyInput:
    issuer_id: Identifier
    title: str
    statements: str
    description: str | None = None


@dataclass(frozen=True)
class CreatePolicyOutput:
    policy: Policy


def create_policy(
    policy_repository: PolicyRepository,
    issuer_repository: IssuerRepository,
    asp_manager: AspManager,
    input_data: CreatePolicyInput
) -> CreatePolicyOutput:
    """
    Add a path-level policy to the service.
    """
    issuer = issuer_repository.get_by_id(input_data.issuer_id)
    if issuer is None:
        raise InvalidInputError(
            "issuer_id", input_data.issuer_id, "Issuer does not exist")

    logging.debug(f"Received publish request from issuer: {issuer.name}")

    try:
        asp_manager.check_syntax(input_data.statements)
    except ValueError:
        raise InvalidInputError(
            "statements", input_data.statements, "Invalid ASP syntax for policy")

    policy = Policy(
        issuer=issuer,
        title=input_data.title,
        statements=input_data.statements,
        description=input_data.description
    )
    policy_repository.add(policy)

    logging.debug(f"Created new policy: {policy.id}")

    return CreatePolicyOutput(policy=policy)


@dataclass(frozen=True)
class UpdatePolicyInput:
    id: Identifier
    title: str | None = None
    statements: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class UpdatePolicyOutput:
    policy: Policy


def update_policy(
    policy_repository: PolicyRepository,
    asp_manager: AspManager,
    input_data: UpdatePolicyInput
) -> UpdatePolicyOutput:
    """
    Update a path-level policy on the service.
    """
    policy = policy_repository.get_by_id(input_data.id)

    if policy is None:
        raise InvalidInputError("id", input_data.id, "No policy with id")

    if input_data.title is not None:
        policy.title = input_data.title

    if input_data.description is not None:
        policy.description = input_data.description

    if input_data.statements is not None:
        try:
            asp_manager.check_syntax(input_data.statements)
            policy.statements = input_data.statements
        except ValueError:
            raise InvalidInputError(
                "statements", input_data.statements, "Invalid ASP syntax for policy")

    policy.updated_at = datetime.now()
    policy_repository.add(policy)

    logging.debug(f"Updated policy: {policy.id}")

    return UpdatePolicyOutput(policy=policy)


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
    meta_policy_repository: MetaPolicyRepository,
    nip_proxy: NipProxy,
    asp_manager: AspManager,
    input_data: ValidatePathInput
) -> ValidatePathOutput:
    """
    Check whether a provided path is valid given the active policies.
    """
    def get_all_readings() -> dict[str, list[HopReading]]:
        energy_readings: list[HopReading] = []
        geo_readings: list[HopReading] = []
        try:
            with ThreadPool(processes=max(1, len(input_data.path.hops))) as pool:
                results = pool.map(
                    partial(
                        nip_proxy.get_readings_for_interval,
                        input_data.interval
                    ),
                    input_data.path.hops
                )
                for result in results:
                    energy_readings.extend(result["energy"])
                    geo_readings.extend(result["geo"])

        except Exception as e:
            raise ExternalServiceError("NipClientService", str(e))

        return {
            "energy": energy_readings,
            "geo": geo_readings
        }

    active_policies = policy_repository.get_all_active()
    readings = get_all_readings()

    logging.debug(f"Validating path: {input_data.path.isd_as_src}->{input_data.path.isd_as_dst}")
    logging.debug(f"\tUsing interval: {input_data.interval.datetime_start}-{input_data.interval.datetime_start}")

    unsat_policies: set[Policy] = set()

    # validate the path using every active policy
    for policy in active_policies:
        valid = asp_manager.validate(policy, input_data.path, readings)
        if not valid:
            unsat_policies.add(policy)

    if len(unsat_policies) == 0:
        return ValidatePathOutput(valid=True)

    meta_policies = meta_policy_repository.get_all_active()
    remaining_unsat_policies = set(unsat_policies)

    with asp_manager.meta(meta_policies) as meta_handle:
        while True:
            for unsat_policy in unsat_policies:
                for other_policy in active_policies:
                    if unsat_policy.id == other_policy.id:
                        continue

                    result = meta_handle.resolve_conflicts(
                        unsat_policy,
                        other_policy
                    )

                    if result.status == ConflictResolutionStatus.NOT_RESOLVED\
                            or result.policy_strong is None:
                        raise RuntimeError(f"Conflict between {unsat_policy} and {other_policy} cannot be solved")

                    if result.policy_strong != unsat_policy and unsat_policy in remaining_unsat_policies:
                        remaining_unsat_policies.remove(unsat_policy)

            if len(unsat_policies) == len(remaining_unsat_policies):
                break

            unsat_policies = remaining_unsat_policies

    return ValidatePathOutput(valid=len(unsat_policies) == 0)


def get_latest_policy_timestamp(
    policy_repository: PolicyRepository,
    meta_policy_repository: MetaPolicyRepository
) -> datetime:
    try:
        latest_policy_tmp = policy_repository\
            .get_max_created_at()\
            .replace(tzinfo=timezone(offset=timedelta()))
        latest_meta_policy_tmp = meta_policy_repository\
            .get_max_created_at()\
            .replace(tzinfo=timezone(offset=timedelta()))
        return max(latest_policy_tmp, latest_meta_policy_tmp)
    except Exception:
        return datetime.now()


def get_default_issuer(issuer_repository: IssuerRepository) -> Issuer:
    issuer = issuer_repository.get_one_default()
    if issuer is None:
        issuer = Issuer(default=True)
        issuer_repository.add(issuer)
    return issuer


def list_all_policies(policy_repository: PolicyRepository) -> list[Policy]:
    return policy_repository.get_all_active()


def get_policy(policy_repository: PolicyRepository, id: Identifier) -> Optional[Policy]:
    return policy_repository.get_by_id(id)


def delete_policy(policy_repository: PolicyRepository, id: Identifier) -> None:
    try:
        logging.debug(f"Deleting policy {id=}")
        return policy_repository.remove(id)
    except Exception as e:
        logging.debug(e)
        raise InvalidInputError("id", id, "No policy with ID")
