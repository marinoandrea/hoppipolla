from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import partial
from multiprocessing.pool import ThreadPool

from policy_manager.domain.entities import (HopReading, Identifier, Path,
                                            Policy, TimeInterval)
from policy_manager.domain.errors import (ExternalServiceError,
                                          InvalidInputError)
from policy_manager.domain.repositories import (IssuerRepository,
                                                MetaPolicyRepository,
                                                PolicyRepository)

from .services import AspManager, ConflictResolutionStatus, NipClientService


@dataclass(frozen=True)
class CreatePolicyInput:
    issuer_id: Identifier
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

    try:
        asp_manager.check_syntax(input_data.statements)
    except ValueError:
        raise InvalidInputError(
            "statements", input_data.statements, "Invalid ASP syntax for policy")

    new_policy = Policy(
        issuer=issuer,
        statements=input_data.statements,
        description=input_data.description
    )
    policy_repository.add(new_policy)

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
    meta_policy_repository: MetaPolicyRepository,
    nip_client_service: NipClientService,
    asp_manager: AspManager,
    input_data: ValidatePathInput
) -> ValidatePathOutput:
    """
    Check whether a provided path is valid given the active policies.
    """
    def get_all_readings() -> list[HopReading]:
        readings: list[HopReading] = []
        try:
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
        return readings

    active_policies = policy_repository.get_all_active()
    readings = get_all_readings()

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
                    if unsat_policy == other_policy:
                        continue

                    result = meta_handle.resolve_conflicts(
                        unsat_policy,
                        other_policy
                    )

                    if result.status == ConflictResolutionStatus.NOT_RESOLVED\
                            or result.policy_strong is None:
                        raise RuntimeError(f"Conflict between {unsat_policy} and {other_policy} cannot be solved")

                    if result.policy_strong != unsat_policy:
                        remaining_unsat_policies.remove(unsat_policy)

            if len(unsat_policies) == len(remaining_unsat_policies):
                break

            unsat_policies = remaining_unsat_policies

    return ValidatePathOutput(valid=len(unsat_policies) == 0)
