from decimal import Decimal

from pydantic import BaseModel


class WalletSchema(BaseModel):
    uuid: str
    balance: Decimal


class WalletBalance(BaseModel):
    balance: Decimal
