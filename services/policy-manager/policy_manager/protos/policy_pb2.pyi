from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import path_pb2 as _path_pb2
import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Issuer(_message.Message):
    __slots__ = ("id", "name", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class Policy(_message.Message):
    __slots__ = ("id", "issuer_id", "active", "statements", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    ISSUER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STATEMENTS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    issuer_id: str
    active: bool
    statements: str
    description: str
    def __init__(self, id: _Optional[str] = ..., issuer_id: _Optional[str] = ..., active: bool = ..., statements: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePolicyRequest(_message.Message):
    __slots__ = ("issuer_id", "statements", "description")
    ISSUER_ID_FIELD_NUMBER: _ClassVar[int]
    STATEMENTS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    issuer_id: str
    statements: str
    description: str
    def __init__(self, issuer_id: _Optional[str] = ..., statements: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePolicyResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePolicyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CreateIssuerRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateIssuerResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ListPoliciesRespose(_message.Message):
    __slots__ = ("policies",)
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[Policy]
    def __init__(self, policies: _Optional[_Iterable[_Union[Policy, _Mapping]]] = ...) -> None: ...

class ValidatePathRequest(_message.Message):
    __slots__ = ("path", "data_interval")
    PATH_FIELD_NUMBER: _ClassVar[int]
    DATA_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    path: _path_pb2.Path
    data_interval: _common_pb2.Interval
    def __init__(self, path: _Optional[_Union[_path_pb2.Path, _Mapping]] = ..., data_interval: _Optional[_Union[_common_pb2.Interval, _Mapping]] = ...) -> None: ...

class ValidatePathResponse(_message.Message):
    __slots__ = ("fingerprint", "valid")
    FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    fingerprint: str
    valid: bool
    def __init__(self, fingerprint: _Optional[str] = ..., valid: bool = ...) -> None: ...

class GetLatestPolicyTimestampResponse(_message.Message):
    __slots__ = ("timestamp",)
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
