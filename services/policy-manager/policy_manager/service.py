from datetime import datetime

from policy_manager.domain.entities import Issuer, Policy
from policy_manager.domain.use_cases import (CreatePolicyInput,
                                             CreatePolicyOutput,
                                             ValidatePathInput,
                                             ValidatePathOutput, create_policy,
                                             get_default_issuer,
                                             get_latest_policy_timestamp,
                                             list_all_policies, validate_path)
from policy_manager.infra.database.vendors.sqlalchemy import get_session
from policy_manager.infra.database.vendors.sqlalchemy.repositories import (
    SQLAlchemyIssuerRepository, SQLAlchemyMetaPolicyRepository,
    SQLAlchemyPolicyRepository)
from policy_manager.locator import ServiceLocator


class PolicyManagerService:

    @staticmethod
    def execute_create_policy(
        input_data: CreatePolicyInput
    ) -> CreatePolicyOutput:
        with get_session() as session:
            try:
                policy_repository = SQLAlchemyPolicyRepository(session)
                issuer_repository = SQLAlchemyIssuerRepository(session)

                output = create_policy(
                    policy_repository,
                    issuer_repository,
                    ServiceLocator.asp_manager,
                    input_data
                )

                session.commit()

                return output

            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def execute_validate_path(
        input_data: ValidatePathInput
    ) -> ValidatePathOutput:
        with get_session() as session:
            try:
                policy_repository = SQLAlchemyPolicyRepository(session)
                meta_policy_repository = SQLAlchemyMetaPolicyRepository(session)

                output = validate_path(
                    policy_repository,
                    meta_policy_repository,
                    ServiceLocator.nip_proxy,
                    ServiceLocator.asp_manager,
                    input_data
                )

                session.commit()

                return output

            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def execute_get_latest_policy_timestamp() -> datetime:
        with get_session() as session:
            try:
                policy_repository = SQLAlchemyPolicyRepository(session)
                meta_policy_repository = SQLAlchemyMetaPolicyRepository(session)
                return get_latest_policy_timestamp(
                    policy_repository,
                    meta_policy_repository
                )
            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def execute_get_default_issuer() -> Issuer:
        with get_session() as session:
            try:
                issuer_repository = SQLAlchemyIssuerRepository(session)
                output = get_default_issuer(issuer_repository)
                session.commit()
                return output
            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def execute_list_all_policies() -> list[Policy]:
        with get_session() as session:
            try:
                policy_repository = SQLAlchemyPolicyRepository(session)
                return list_all_policies(policy_repository)
            except Exception as e:
                session.rollback()
                raise e
