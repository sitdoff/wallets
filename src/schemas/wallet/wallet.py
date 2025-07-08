from decimal import Decimal

from pydantic import BaseModel


class WalletSchema(BaseModel):
    """
    Схема кошелька.
    """

    uuid: str
    balance: Decimal


class WalletBalance(BaseModel):
    """
    Схема баланса кошелька.
    """

    balance: Decimal
