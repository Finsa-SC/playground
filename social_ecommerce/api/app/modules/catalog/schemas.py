from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=20000)
    price: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    currency: str = Field(default="IDR", pattern=r"^[A-Z]{3}$")
    stock_quantity: int = Field(default=1, ge=0)
    category_id: UUID | None = None


class ProductUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=20000)
    price: Decimal | None = Field(default=None, gt=0, max_digits=18, decimal_places=2)
    stock_quantity: int | None = Field(default=None, ge=0)
    category_id: UUID | None = None
