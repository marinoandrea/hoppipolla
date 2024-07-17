import logging
import os
from dataclasses import dataclass


@dataclass
class Config:
    env: str
    host: str
    port: int
    log_level: int
    n_workers: int
    database_uri: str
    nip_proxy_uri: str


config = Config(
    env=os.environ.get("ENV", "development"),
    host=os.environ.get("HOST", "0.0.0.0"),
    port=int(os.environ.get("PORT", "27002")),
    log_level=int(os.environ.get("LOG_LEVEL", logging.INFO)),
    n_workers=int(os.environ.get("MAX_WORKERS", 10)),
    nip_proxy_uri=os.environ.get("NIP_PROXY_URI", "localhost:27003"),
    database_uri=os.environ.get("DATABASE_URI", "postgresql://postgres:test@127.0.0.1:5432/postgres")
)
