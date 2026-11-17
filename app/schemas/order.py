
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    customer_id: int
    product_name: str
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    product_name: str
    amount: Decimal
    status: str
    created_at: datetime
