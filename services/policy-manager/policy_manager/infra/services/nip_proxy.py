from typing import Any, Callable, Dict, Self, Type, TypeVar, cast

import grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp
from policy_manager.config import config
from policy_manager.domain.entities import Hop, HopReading, TimeInterval
from policy_manager.domain.services import NipProxy
from policy_manager.protos.common_pb2 import Interval
from policy_manager.protos.nip_pb2 import (GetEnergyReadingsRequest,
                                           GetEnergyReadingsResponse)
from policy_manager.protos.nip_pb2_grpc import NipProxyStub

T = TypeVar('T')


def singleton(cls: Type[T]) -> Callable[..., T]:
    instances: Dict[Type, T] = {}

    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class NipProxyGRPCService(NipProxy):
    _instance: Self | None = None

    def __init__(self, addr: str = config.nip_proxy_uri) -> None:
        self.channel = grpc.insecure_channel(addr)
        self.client = NipProxyStub(self.channel)

    def get_readings_for_interval(
            self, interval: TimeInterval, hop: Hop) -> list[HopReading]:

        start_time = Timestamp()
        start_time.FromDatetime(interval.datetime_start)
        end_time = Timestamp()
        end_time.FromDatetime(interval.datetime_end)

        req = GetEnergyReadingsRequest(
            isd_as=hop.isd_as,
            interval=Interval(start_time, end_time)
        )

        res = cast(GetEnergyReadingsResponse,
                   self.client.GetEnergyReadings(req))

        return [MessageToDict(entry) for entry in res.data]
