from typing import Generic, TypeVar

TValue = TypeVar("TValue")


class InvalidInputError(ValueError, Generic[TValue]):
    field: str
    value: TValue
    reason: str

    def __init__(self, field: str, value: TValue, reason: str) -> None:
        super().__init__(f"Input field '{field}' is invalid: {reason}")
        self.field = field
        self.value = value
        self.reason = reason


class ExternalServiceError(RuntimeError):
    service: str
    reason: str

    def __init__(self, service: str, reason: str) -> None:
        super().__init__(f"Service '{service}' returned an error: {reason}")
        self.service = service
        self.reason = reason
