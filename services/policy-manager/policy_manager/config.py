import os
from dataclasses import dataclass

from policy_manager.domain.services import AspManager, NipClientService
from policy_manager.infra.services.asp import ClingoAspManager
from policy_manager.infra.services.nip_client import NipClientGRPCService


@dataclass
class Config:
    env: str
    database_uri: str
    nip_client_address: str


config = Config(
    env=os.environ.get("POLICY_MANAGER_ENV", "development"),
    nip_client_address=os.environ.get("NIP_CLIENT_ADDRESS", "localhost:9002"),
    database_uri=os.environ.get(
        "POLICY_MANAGER_DATABASE_URI",
        "sqlite:///~/.local/share/hoppipolla/policy-manager/sqlite.db"),
)


@dataclass
class ServiceLocator:
    nip_client: NipClientService
    asp_manager: AspManager


ServiceLocator.nip_client = NipClientGRPCService(config.nip_client_address)
ServiceLocator.asp_manager = ClingoAspManager()
