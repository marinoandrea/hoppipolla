import uuid

import pytest
from policy_manager.domain.errors import InvalidInputError
from policy_manager.domain.use_cases import CreatePolicyInput, create_policy
from policy_manager.infra.database.vendors.in_memory.repositories import (
    InMemoryIssuerRepository, InMemoryPolicyRepository)
from policy_manager.infra.services.asp import ClingoAspManager


def test_raises_error_on_missing_issuer():
    policy_repository = InMemoryPolicyRepository()
    issuer_repository = InMemoryIssuerRepository()
    asp_manager = ClingoAspManager()

    input_data = CreatePolicyInput(
        issuer_id=uuid.uuid4(),
        statements=""
    )

    with pytest.raises(InvalidInputError):
        create_policy(
            policy_repository=policy_repository,
            issuer_repository=issuer_repository,
            asp_manager=asp_manager,
            input_data=input_data
        )
