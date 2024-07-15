from dataclasses import dataclass

from policy_manager.domain.services import AspManager, NipClientService
from policy_manager.infra.services.asp import ClingoAspManager
from policy_manager.infra.services.nip_client import NipClientGRPCService

from .config import config


@dataclass
class ServiceLocator:
    nip_client: NipClientService
    asp_manager: AspManager


ServiceLocator.nip_client = NipClientGRPCService(config.nip_client_address)
ServiceLocator.asp_manager = ClingoAspManager()
