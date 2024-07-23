from google.protobuf import empty_pb2 as _empty_pb2
import path_pb2 as _path_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Issuer(_message.Message):
    __slots__ = ("id", "created_at", "updated_at", "name", "default", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    created_at: str
    updated_at: str
    name: str
    default: bool
    description: str
    def __init__(self, id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., name: _Optional[str] = ..., default: bool = ..., description: _Optional[str] = ...) -> None: ...

class Policy(_message.Message):
    __slots__ = ("id", "created_at", "updated_at", "issuer", "active", "statements", "title", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STATEMENTS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    created_at: str
    updated_at: str
    issuer: Issuer
    active: bool
    statements: str
    title: str
    description: str
    def __init__(self, id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., issuer: _Optional[_Union[Issuer, _Mapping]] = ..., active: bool = ..., statements: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePolicyRequest(_message.Message):
    __slots__ = ("issuer_id", "statements", "title", "description")
    ISSUER_ID_FIELD_NUMBER: _ClassVar[int]
    STATEMENTS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    issuer_id: str
    statements: str
    title: str
    description: str
    def __init__(self, issuer_id: _Optional[str] = ..., statements: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: Policy
    def __init__(self, policy: _Optional[_Union[Policy, _Mapping]] = ...) -> None: ...

class UpdatePolicyRequest(_message.Message):
    __slots__ = ("id", "statements", "title", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATEMENTS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    statements: str
    title: str
    description: str
    def __init__(self, id: _Optional[str] = ..., statements: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class UpdatePolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: Policy
    def __init__(self, policy: _Optional[_Union[Policy, _Mapping]] = ...) -> None: ...

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
    __slots__ = ("issuer",)
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    issuer: Issuer
    def __init__(self, issuer: _Optional[_Union[Issuer, _Mapping]] = ...) -> None: ...

class GetPolicyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetPolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: Policy
    def __init__(self, policy: _Optional[_Union[Policy, _Mapping]] = ...) -> None: ...

class ListPoliciesResponse(_message.Message):
    __slots__ = ("policies",)
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[Policy]
    def __init__(self, policies: _Optional[_Iterable[_Union[Policy, _Mapping]]] = ...) -> None: ...

class ValidatePathRequest(_message.Message):
    __slots__ = ("path", "start_time", "end_time")
    PATH_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    path: _path_pb2.Path
    start_time: str
    end_time: str
    def __init__(self, path: _Optional[_Union[_path_pb2.Path, _Mapping]] = ..., start_time: _Optional[str] = ..., end_time: _Optional[str] = ...) -> None: ...

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
    timestamp: str
    def __init__(self, timestamp: _Optional[str] = ...) -> None: ...

class GetDefaultIssuerResponse(_message.Message):
    __slots__ = ("issuer",)
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    issuer: Issuer
    def __init__(self, issuer: _Optional[_Union[Issuer, _Mapping]] = ...) -> None: ...
