from dataclasses import dataclass

from policy_manager.domain.services import AspManager, NipProxy
from policy_manager.infra.services.asp import ClingoAspManager
from policy_manager.infra.services.nip_proxy import NipProxyGRPCService

from .config import config


@dataclass
class ServiceLocator:
    nip_client: NipProxy
    asp_manager: AspManager


ServiceLocator.nip_client = NipProxyGRPCService(config.nip_proxy_uri)
ServiceLocator.asp_manager = ClingoAspManager()
