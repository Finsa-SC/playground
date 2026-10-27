from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None

class CategoryOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None

class ProductCreate(BaseModel):
    category_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    is_available: bool = True

class ProductUpdate(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    stock_quantity: int | None = Field(default=None, ge=0)
    is_available: bool | None = None

class ImageOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    alt_text: str | None
    is_primary: bool

class ProductOutput(BaseModel):
    id: int
    category_id: int
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    is_available: bool
    images: list[ImageOutput]
