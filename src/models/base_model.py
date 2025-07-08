from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class BaseModel(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.convention)
