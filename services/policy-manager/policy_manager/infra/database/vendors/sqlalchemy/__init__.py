import sqlalchemy
from policy_manager.config import config
from sqlalchemy.orm import Session

from .models import BaseModel

is_debug = config.env == "development"

engine = sqlalchemy.create_engine(config.database_uri, echo=is_debug)


def get_session():
    return Session(engine)


BaseModel.metadata.create_all(engine)
