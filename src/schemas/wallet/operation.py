from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class OperationSchema(BaseModel):
    """
    Схема операции с кошельком.
    """

    operation_type: Literal["DEPOSIT", "WITHDRAW"]
    amount: Decimal = Field(gt=0)
