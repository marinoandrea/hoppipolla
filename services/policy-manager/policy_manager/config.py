import logging
import os
from dataclasses import dataclass


@dataclass
class Config:
    env: str
    host: str
    port: int
    log_level: int
    database_uri: str
    nip_client_address: str


config = Config(
    env=os.environ.get("ENV", "development"),
    host=os.environ.get("HOST", "localhost:27002"),
    port=int(os.environ.get("PORT", "localhost:27002")),
    log_level=int(os.environ.get("LOG_LEVEL", logging.INFO)),
    nip_client_address=os.environ.get("NIP_CLIENT_ADDRESS", "localhost:27003"),
    database_uri=os.environ.get("DATABASE_URI", "postgres://localhost:5432/postgres")
)
