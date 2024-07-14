import logging
from abc import ABCMeta
from functools import wraps
from typing import Optional, cast

import grpc
from google.protobuf.empty_pb2 import Empty

from .errors import (HoppipollaServiceInitializationError,
                     HoppipollaServiceRequestMaxRetriesError)
from .protos.path_pb2 import GetPathsForAddrRequest, GetPathsForAddrResponse
from .protos.path_pb2_grpc import PathAnalyzerStub
from .protos.policy_pb2 import (CreatePolicyRequest, CreatePolicyResponse,
                                DeletePolicyRequest, GetDefaultIssuerResponse)
from .protos.policy_pb2_grpc import PolicyManagerStub
from .services import (HoppipollaServiceClient, PathAnalyzerClient,
                       PolicyManagerClient)
from .types import ConnectionConfig, Issuer, LoggingConfig, Path, Policy


class GRPCHoppipollaServiceClient(HoppipollaServiceClient, metaclass=ABCMeta):
    def __init__(self, config: ConnectionConfig, logging_config: LoggingConfig) -> None:
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.level = logging_config.level
        try:
            self.channel = grpc.insecure_channel(config.base_url)
        except Exception as e:
            raise HoppipollaServiceInitializationError(self.service_name, str(e))


def with_retries(func):
    @wraps(func)
    def wrapper(self: GRPCHoppipollaServiceClient, *args, **kwargs):
        attempt = 0
        while attempt < self.config.n_retries:
            self.logger.debug(f"request attempt #{attempt}")
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.logger.error(e)
                attempt += 1
                if attempt >= self.config.n_retries:
                    raise HoppipollaServiceRequestMaxRetriesError(
                        self.service_name,
                        f"executed max number of {self.config.n_retries} retries"
                    )
    return wrapper


class GRPCPathAnalyzerClient(GRPCHoppipollaServiceClient, PathAnalyzerClient):

    def __init__(self, config: ConnectionConfig, logging_config: LoggingConfig) -> None:
        super().__init__(config, logging_config)
        self.client = PathAnalyzerStub(self.channel)

    @with_retries
    def get_path_for_address(self, address: str) -> Optional[Path]:
        req = GetPathsForAddrRequest(destination=address)
        res = cast(GetPathsForAddrResponse, self.client.GetPathsForAddr(req))

        if len(res.paths) == 0:
            self.logger.info(f"no valid paths for {address}")
            return None

        path = res.paths[0]
        self.logger.info(f"selected path '{path.fingerprint}' for {address}")

        return Path(
            fingerprint=path.fingerprint,
            destination=path.dst_isd_as,
            sequence=path.sequence
        )


class GRPCPolicyManagerClient(GRPCHoppipollaServiceClient, PolicyManagerClient):

    def __init__(self, config: ConnectionConfig, logging_config: LoggingConfig) -> None:
        super().__init__(config, logging_config)
        self.client = PolicyManagerStub(self.channel)
        self._default_issuer: Optional[Issuer] = None

    @property
    @with_retries
    def default_issuer(self) -> Issuer:
        if self._default_issuer is None:
            req = Empty()
            res = cast(GetDefaultIssuerResponse, self.client.GetDefaultIssuer(req))
            self.logger.info(f"retrieved default issuer with id '{res.id}'")
            self._default_issuer = Issuer(
                id=res.id,
                name=res.name,
                description=res.description
            )
        return self._default_issuer

    @with_retries
    def publish_policy(self, issuer: Issuer, statements: str) -> Policy:
        req = CreatePolicyRequest(issuer_id=issuer.id, statements=statements)
        res = cast(CreatePolicyResponse, self.client.CreatePolicy(req))
        self.logger.info(f"published policy with id '{res.id}'")
        return Policy(id=res.id, issuer_id=issuer.id, statements=statements)

    @with_retries
    def delete_policy(self, policy_id: str) -> None:
        req = DeletePolicyRequest(id=policy_id)
        self.logger.info(f"deleted policy with id '{policy_id}'")
        self.client.DeletePolicy(req)
