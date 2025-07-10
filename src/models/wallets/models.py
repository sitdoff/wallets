import uuid as python_uuid
from decimal import Decimal

from sqlalchemy import DECIMAL
from sqlalchemy import UUID as ac_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel


class WalletModel(BaseModel):
    """
    Модель кошелька для базы данных.
    """

    __tablename__ = "wallets"

    uuid: Mapped[python_uuid.UUID] = mapped_column(
        ac_UUID(as_uuid=True),
        primary_key=True,
        default=python_uuid.uuid4,
    )
    balance: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=12, scale=2),
        default=Decimal("0.00"),
        nullable=False,
    )
