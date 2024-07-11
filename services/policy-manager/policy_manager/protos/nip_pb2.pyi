from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HopData(_message.Message):
    __slots__ = ("isd_as", "total_energy_consumption", "peak_energy_consumption", "off_peak_energy_consumption", "energy_consumption_per_hour", "renewable_energy_consumption", "non_renewable_energy_consumption", "co2_emissions", "renewable_energy_percentage", "uptime", "downtime", "maintenance_frequency", "energy_efficiency_rating", "sustainability_index", "carbon_footprint_reduction", "last_maintenance_date", "data_collected_date", "location")
    ISD_AS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ENERGY_CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    PEAK_ENERGY_CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    OFF_PEAK_ENERGY_CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    ENERGY_CONSUMPTION_PER_HOUR_FIELD_NUMBER: _ClassVar[int]
    RENEWABLE_ENERGY_CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    NON_RENEWABLE_ENERGY_CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    CO2_EMISSIONS_FIELD_NUMBER: _ClassVar[int]
    RENEWABLE_ENERGY_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    UPTIME_FIELD_NUMBER: _ClassVar[int]
    DOWNTIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    ENERGY_EFFICIENCY_RATING_FIELD_NUMBER: _ClassVar[int]
    SUSTAINABILITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    CARBON_FOOTPRINT_REDUCTION_FIELD_NUMBER: _ClassVar[int]
    LAST_MAINTENANCE_DATE_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTED_DATE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    isd_as: str
    total_energy_consumption: float
    peak_energy_consumption: float
    off_peak_energy_consumption: float
    energy_consumption_per_hour: float
    renewable_energy_consumption: float
    non_renewable_energy_consumption: float
    co2_emissions: float
    renewable_energy_percentage: float
    uptime: float
    downtime: float
    maintenance_frequency: float
    energy_efficiency_rating: float
    sustainability_index: float
    carbon_footprint_reduction: float
    last_maintenance_date: _timestamp_pb2.Timestamp
    data_collected_date: _timestamp_pb2.Timestamp
    location: str
    def __init__(self, isd_as: _Optional[str] = ..., total_energy_consumption: _Optional[float] = ..., peak_energy_consumption: _Optional[float] = ..., off_peak_energy_consumption: _Optional[float] = ..., energy_consumption_per_hour: _Optional[float] = ..., renewable_energy_consumption: _Optional[float] = ..., non_renewable_energy_consumption: _Optional[float] = ..., co2_emissions: _Optional[float] = ..., renewable_energy_percentage: _Optional[float] = ..., uptime: _Optional[float] = ..., downtime: _Optional[float] = ..., maintenance_frequency: _Optional[float] = ..., energy_efficiency_rating: _Optional[float] = ..., sustainability_index: _Optional[float] = ..., carbon_footprint_reduction: _Optional[float] = ..., last_maintenance_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_collected_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., location: _Optional[str] = ...) -> None: ...

class GetLatestHopDataRequest(_message.Message):
    __slots__ = ("isd_as",)
    ISD_AS_FIELD_NUMBER: _ClassVar[int]
    isd_as: str
    def __init__(self, isd_as: _Optional[str] = ...) -> None: ...

class GetAggregatedHopDataRequest(_message.Message):
    __slots__ = ("isd_as", "interval")
    ISD_AS_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    isd_as: str
    interval: _common_pb2.Interval
    def __init__(self, isd_as: _Optional[str] = ..., interval: _Optional[_Union[_common_pb2.Interval, _Mapping]] = ...) -> None: ...

class GetHopDataForIntervalRequest(_message.Message):
    __slots__ = ("isd_as", "interval")
    ISD_AS_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    isd_as: str
    interval: _common_pb2.Interval
    def __init__(self, isd_as: _Optional[str] = ..., interval: _Optional[_Union[_common_pb2.Interval, _Mapping]] = ...) -> None: ...

class GetHopDataForIntervalResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[HopData]
    def __init__(self, data: _Optional[_Iterable[_Union[HopData, _Mapping]]] = ...) -> None: ...
