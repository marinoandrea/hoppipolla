from policy_manager.config import ServiceLocator
from policy_manager.domain.use_cases import (CreatePolicyInput,
                                             CreatePolicyOutput,
                                             ValidatePathInput,
                                             ValidatePathOutput, create_policy,
                                             validate_path)
from policy_manager.infra.database.vendors.sqlalchemy import get_session
from policy_manager.infra.database.vendors.sqlalchemy.repositories import (
    SQLAlchemyIssuerRepository, SQLAlchemyMetaPolicyRepository,
    SQLAlchemyPolicyRepository)


class PolicyManagerService:

    @staticmethod
    def execute_create_policy(
        input_data: CreatePolicyInput
    ) -> CreatePolicyOutput:
        with get_session() as session:
            try:
                policy_repository = SQLAlchemyPolicyRepository(session)
                issuer_repository = SQLAlchemyIssuerRepository(session)
                meta_policy_repository = SQLAlchemyMetaPolicyRepository(
                    session)

                output = create_policy(
                    policy_repository,
                    issuer_repository,
                    meta_policy_repository,
                    ServiceLocator.asp_manager,
                    input_data
                )

                policy_repository.persist_all()
                issuer_repository.persist_all()

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

                output = validate_path(
                    policy_repository,
                    ServiceLocator.nip_client,
                    ServiceLocator.asp_manager,
                    input_data
                )

                policy_repository.persist_all()

                return output

            except Exception as e:
                session.rollback()
                raise e
