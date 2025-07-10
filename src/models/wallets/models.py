from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DECIMAL, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel


class WalletModel(BaseModel):
    """
    Модель кошелька для базы данных.
    """

    __tablename__ = "wallets"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    balance: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=12, scale=2),
        default=Decimal("0.00"),
        nullable=False,
    )
