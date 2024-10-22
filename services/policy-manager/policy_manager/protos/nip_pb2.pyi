from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnergyReading(_message.Message):
    __slots__ = ("id", "isd_as", "machine_id", "collected_at", "energy_consumption_kWh", "cpu_usage_percentage", "memory_usage_percentage", "network_traffic_MB", "temperature_celsius", "power_source", "status", "carbon_emissions_kg", "renewable_energy_percentage", "energy_efficiency_rating")
    ID_FIELD_NUMBER: _ClassVar[int]
    ISD_AS_FIELD_NUMBER: _ClassVar[int]
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTED_AT_FIELD_NUMBER: _ClassVar[int]
    ENERGY_CONSUMPTION_KWH_FIELD_NUMBER: _ClassVar[int]
    CPU_USAGE_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USAGE_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_TRAFFIC_MB_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_CELSIUS_FIELD_NUMBER: _ClassVar[int]
    POWER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CARBON_EMISSIONS_KG_FIELD_NUMBER: _ClassVar[int]
    RENEWABLE_ENERGY_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    ENERGY_EFFICIENCY_RATING_FIELD_NUMBER: _ClassVar[int]
    id: str
    isd_as: str
    machine_id: str
    collected_at: _timestamp_pb2.Timestamp
    energy_consumption_kWh: float
    cpu_usage_percentage: float
    memory_usage_percentage: float
    network_traffic_MB: float
    temperature_celsius: float
    power_source: str
    status: str
    carbon_emissions_kg: float
    renewable_energy_percentage: float
    energy_efficiency_rating: str
    def __init__(self, id: _Optional[str] = ..., isd_as: _Optional[str] = ..., machine_id: _Optional[str] = ..., collected_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., energy_consumption_kWh: _Optional[float] = ..., cpu_usage_percentage: _Optional[float] = ..., memory_usage_percentage: _Optional[float] = ..., network_traffic_MB: _Optional[float] = ..., temperature_celsius: _Optional[float] = ..., power_source: _Optional[str] = ..., status: _Optional[str] = ..., carbon_emissions_kg: _Optional[float] = ..., renewable_energy_percentage: _Optional[float] = ..., energy_efficiency_rating: _Optional[str] = ...) -> None: ...

class GetEnergyReadingsRequest(_message.Message):
    __slots__ = ("isd_as", "interval")
    ISD_AS_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    isd_as: str
    interval: _common_pb2.Interval
    def __init__(self, isd_as: _Optional[str] = ..., interval: _Optional[_Union[_common_pb2.Interval, _Mapping]] = ...) -> None: ...

class GetEnergyReadingsResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[EnergyReading]
    def __init__(self, data: _Optional[_Iterable[_Union[EnergyReading, _Mapping]]] = ...) -> None: ...
