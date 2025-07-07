from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class OperationSchema(BaseModel):
    operation_type: Literal["DEPOSIT", "WITHDRAW"]
    amount: Decimal
