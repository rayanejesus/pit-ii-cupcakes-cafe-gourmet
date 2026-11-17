from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    image_url: str
    ingredients: str
    allergens: str
    available: bool
    category_id: int
    category: CategoryResponse


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=2)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)
    image_url: str = Field(min_length=1)
    ingredients: str
    allergens: str
    available: bool = True
    category_id: int = Field(gt=0)
