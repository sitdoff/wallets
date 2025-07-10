from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class WalletSchema(BaseModel):
    """
    Схема кошелька.
    """

    uuid: UUID
    balance: Decimal


class WalletBalance(BaseModel):
    """
    Схема баланса кошелька.
    """

    balance: Decimal
