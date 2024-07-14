'''
Error Hierarchy
---------------
The class hierarchy for the Hoppipolla errors is:

```
HoppipollaError
├── HoppipollaServiceError
│   ├── HoppipollaServiceInitalizationError
│   └── HoppipollaServiceRequestError
│       ├── HoppipollaServiceRequestTimeoutError
│       └── HoppipollaServiceRequestMaxRetriesError
└── HoppipollaScionError
```
'''
from abc import ABCMeta


class HoppipollaError(Exception, metaclass=ABCMeta):
    """
    Base class for all Hoppipolla SDK exceptions.
    """
    ...


class HoppipollaServiceError(HoppipollaError):
    """
    Base class for all Hoppipolla SDK exceptions related to requests to the
    services of the frameworks' stack.
    """

    def __init__(self, service_name: str, msg: str) -> None:
        super().__init__(f"{service_name}: {msg}")
        self.service_name = service_name
        self.msg = msg


class HoppipollaServiceInitializationError(HoppipollaServiceError):
    """
    Exception raised when a Hoppipolla service client fails to initialize.
    """
    ...


class HoppipollaServiceRequestError(HoppipollaServiceError):
    """
    Exception raised when a Hoppipolla service client request fails.
    """
    ...


class HoppipollaServiceRequestMaxRetriesError(HoppipollaServiceRequestError):
    """
    Exception raised when a Hoppipolla service client request fails due to
    hitting the max retries limit that was previously configured.
    """
    ...


class HoppipollaServiceRequestTimeoutError(HoppipollaServiceRequestError):
    """
    Exception raised when a Hoppipolla service client request fails due to
    hitting the timeout that was previously configured.
    """
    ...


class HoppipollaScionError(HoppipollaError):
    """
    Base class for all SCION network utlities used by the Hoppipolla SDK.
    """
    ...
