from typing import Any, Callable, Dict, Self, Type, TypeVar, cast

import grpc
from google.protobuf.json_format import MessageToDict
from policy_manager.config import config
from policy_manager.domain.entities import Hop, HopReading, TimeInterval
from policy_manager.domain.services import NipProxy
from policy_manager.protos.nip_pb2 import (GetEnergyReadingsRequest,
                                           GetEnergyReadingsResponse,
                                           GetGeoReadingsRequest,
                                           GetGeoReadingsResponse)
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
            self, interval: TimeInterval, hop: Hop) -> dict[str, list[HopReading]]:

        start_time = interval.datetime_start.astimezone().isoformat(timespec="milliseconds")
        end_time = interval.datetime_end.astimezone().isoformat(timespec="milliseconds")

        energy_req = GetEnergyReadingsRequest(
            isd_as=hop.isd_as,
            start_time=start_time,
            end_time=end_time,
        )

        energy_res = cast(
            GetEnergyReadingsResponse,
            self.client.GetEnergyReadings(energy_req)
        )

        geo_req = GetGeoReadingsRequest(
            isd_as=hop.isd_as,
            start_time=start_time,
            end_time=end_time,
        )

        geo_res = cast(
            GetGeoReadingsResponse,
            self.client.GetGeoReadings(geo_req)
        )

        return {
            "energy": [MessageToDict(entry) for entry in energy_res.data],
            "geo": [MessageToDict(entry) for entry in geo_res.data],
        }
