from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Hop(_message.Message):
    __slots__ = ("isd_as", "inbound_interface", "outbound_interface")
    ISD_AS_FIELD_NUMBER: _ClassVar[int]
    INBOUND_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    OUTBOUND_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    isd_as: str
    inbound_interface: int
    outbound_interface: int
    def __init__(self, isd_as: _Optional[str] = ..., inbound_interface: _Optional[int] = ..., outbound_interface: _Optional[int] = ...) -> None: ...

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
    expiration: str
    mtu: int
    hops: _containers.RepeatedCompositeFieldContainer[Hop]
    def __init__(self, fingerprint: _Optional[str] = ..., src_isd_as: _Optional[str] = ..., dst_isd_as: _Optional[str] = ..., sequence: _Optional[str] = ..., expiration: _Optional[str] = ..., mtu: _Optional[int] = ..., hops: _Optional[_Iterable[_Union[Hop, _Mapping]]] = ...) -> None: ...

class GetPathForAddrRequest(_message.Message):
    __slots__ = ("destination",)
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    destination: str
    def __init__(self, destination: _Optional[str] = ...) -> None: ...

class GetPathForAddrResponse(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: Path
    def __init__(self, path: _Optional[_Union[Path, _Mapping]] = ...) -> None: ...
