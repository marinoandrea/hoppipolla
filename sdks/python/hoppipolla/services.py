from abc import ABCMeta, abstractmethod
from typing import Optional

from .types import Issuer, Path, Policy


class HoppipollaServiceClient(metaclass=ABCMeta):
    service_name: str


class PathAnalyzerClient(HoppipollaServiceClient, metaclass=ABCMeta):
    service_name = "path-analyzer"

    @abstractmethod
    def get_path_for_address(self, address: str) -> Optional[Path]:
        ...


class PolicyManagerClient(HoppipollaServiceClient, metaclass=ABCMeta):
    service_name = "policy-manager"

    @property
    @abstractmethod
    def default_issuer(self) -> Issuer:
        ...

    @abstractmethod
    def publish_policy(self, issuer: Issuer, statements: str) -> Policy:
        ...

    @abstractmethod
    def delete_policy(self, policy_id: str) -> None:
        ...
