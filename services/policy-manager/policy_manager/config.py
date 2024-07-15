import os
from dataclasses import dataclass


@dataclass
class Config:
    env: str
    database_uri: str
    nip_client_address: str


config = Config(
    env=os.environ.get("ENV", "development"),
    nip_client_address=os.environ.get("NIP_CLIENT_ADDRESS", "localhost:27002"),
    database_uri=os.environ.get(
        "POLICY_MANAGER_DATABASE_URI",
        "sqlite:///~/.local/share/hoppipolla/policy-manager/sqlite.db"),
)
