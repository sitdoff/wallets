import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.utils import BaseModel


class WalletModel(BaseModel):
    __tablename__ = "wallet"

    uuid: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    balance: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=12, scale=2),
        default=Decimal("0.00"),
        nullable=False,
    )
