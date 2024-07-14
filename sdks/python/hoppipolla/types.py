import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class ConnectionConfig:
    base_url: str
    timeout_ms: int = 20_000
    n_retries: int = 3


@dataclass
class LoggingConfig:
    level: int = logging.INFO
    file: str | None = None
    debug: bool = False


@dataclass(frozen=True)
class DataCollectionTimeInterval:
    start: datetime = field(default_factory=datetime.now)
    end: datetime = field(default_factory=lambda: datetime.now() - timedelta(days=7))


@dataclass(frozen=True)
class Issuer:
    id: str
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class Policy:
    id: str
    issuer_id: str
    statements: str
    description: str | None = None


@dataclass(frozen=True)
class Hop:
    isd_as: str
    ifid: Optional[str] = None


@dataclass(frozen=True)
class Path:
    fingerprint: str
    destination: str
    sequence: str


@dataclass(frozen=True)
class PingResult:
    success: bool
    path: Optional[Path]
