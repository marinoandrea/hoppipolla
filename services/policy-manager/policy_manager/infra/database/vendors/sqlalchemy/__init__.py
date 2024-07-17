import sqlalchemy
from policy_manager.config import config
from sqlalchemy.orm import Session

from .models import BaseModel

engine = sqlalchemy.create_engine(config.database_uri, echo=False)


def get_session():
    return Session(engine)


BaseModel.metadata.create_all(engine)
