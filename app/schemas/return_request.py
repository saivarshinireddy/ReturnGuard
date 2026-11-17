
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReturnRequestCreate(BaseModel):
    order_id: int
    reason: str = Field(min_length=10, max_length=1000)


class ReturnRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    reason: str
    status: str
    created_at: datetime
