from typing import Any, Callable, Dict, Self, Type, TypeVar, cast

import grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp
from policy_manager.config import config
from policy_manager.domain.entities import Hop, HopReading, TimeInterval
from policy_manager.domain.services import NipClientService
from policy_manager.protos.common_pb2 import Interval
from policy_manager.protos.nip_pb2 import (GetHopDataForIntervalRequest,
                                           GetHopDataForIntervalResponse)
from policy_manager.protos.nip_pb2_grpc import NipClientStub

T = TypeVar('T')


def singleton(cls: Type[T]) -> Callable[..., T]:
    instances: Dict[Type, T] = {}

    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class NipClientGRPCService(NipClientService):
    channel: grpc.Channel
    client: NipClientStub

    _instance: Self | None = None

    def __init__(self, addr: str = config.nip_client_address) -> None:
        self.channel = grpc.insecure_channel(addr)
        self.client = NipClientStub(self.channel)

    def get_readings_for_interval(
            self, interval: TimeInterval, hop: Hop) -> list[HopReading]:

        start_time = Timestamp()
        start_time.FromDatetime(interval.datetime_start)
        end_time = Timestamp()
        end_time.FromDatetime(interval.datetime_end)

        req = GetHopDataForIntervalRequest(
            isd_as=hop.isd_as,
            interval=Interval(start_time, end_time)
        )

        res = cast(GetHopDataForIntervalResponse,
                   self.client.GetHopDataForInterval(req))

        return [MessageToDict(entry) for entry in res.data]
