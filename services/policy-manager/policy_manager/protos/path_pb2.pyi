from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Hop(_message.Message):
    __slots__ = ("isd_as", "ifid")
    ISD_AS_FIELD_NUMBER: _ClassVar[int]
    IFID_FIELD_NUMBER: _ClassVar[int]
    isd_as: str
    ifid: str
    def __init__(self, isd_as: _Optional[str] = ..., ifid: _Optional[str] = ...) -> None: ...

class Path(_message.Message):
    __slots__ = ("fingerprint", "src_isd_as", "dst_isd_as", "sequence", "expiration", "mtu", "hops")
    FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    SRC_ISD_AS_FIELD_NUMBER: _ClassVar[int]
    DST_ISD_AS_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    MTU_FIELD_NUMBER: _ClassVar[int]
    HOPS_FIELD_NUMBER: _ClassVar[int]
    fingerprint: str
    src_isd_as: str
    dst_isd_as: str
    sequence: str
    expiration: _timestamp_pb2.Timestamp
    mtu: int
    hops: _containers.RepeatedCompositeFieldContainer[Hop]
    def __init__(self, fingerprint: _Optional[str] = ..., src_isd_as: _Optional[str] = ..., dst_isd_as: _Optional[str] = ..., sequence: _Optional[str] = ..., expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mtu: _Optional[int] = ..., hops: _Optional[_Iterable[_Union[Hop, _Mapping]]] = ...) -> None: ...

class GetPathsForAddrRequest(_message.Message):
    __slots__ = ("destination",)
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    destination: str
    def __init__(self, destination: _Optional[str] = ...) -> None: ...

class GetPathsForAddrResponse(_message.Message):
    __slots__ = ("paths",)
    PATHS_FIELD_NUMBER: _ClassVar[int]
    paths: _containers.RepeatedCompositeFieldContainer[Path]
    def __init__(self, paths: _Optional[_Iterable[_Union[Path, _Mapping]]] = ...) -> None: ...
