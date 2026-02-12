from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    quantity: int = Field(..., ge=0, description="Left in stock")
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    category_id: int


class ProductCreate(ProductBase):
    sku: str | None = Field(None, max_length=50)


class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    quantity: int | None = Field(None, ge=0)
    price: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    category_id: int | None = None
    sku: str | None = Field(None, max_length=50)


class ProductResponse(ProductBase):
    id: int
    sku: str

    model_config = ConfigDict(from_attributes=True)
