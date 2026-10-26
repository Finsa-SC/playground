from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class OrderItemInput(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=1000)

class OrderCreate(BaseModel):
    items: list[OrderItemInput] = Field(min_length=1, max_length=50)

class OrderItemOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal

class OrderOutput(BaseModel):
    id: int
    customer_id: int | None
    status: str
    total_amount: Decimal
    created_at: datetime
    items: list[OrderItemOutput]

class OrderStatusUpdate(BaseModel):
    status: str = Field(pattern="^(pending|confirmed|preparing|completed|cancelled)$")
