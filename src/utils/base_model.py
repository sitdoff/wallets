from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import settings


class AppBaseModel(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.convention)

    id: Mapped[int] = mapped_column(primary_key=True)
