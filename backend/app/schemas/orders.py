from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.orders import OrderStatus, PaymentMethod


class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=50)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    customer_email: EmailStr
    address: str = Field(min_length=8, max_length=300)
    payment_method: PaymentMethod
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_name: str
    customer_email: str
    address: str
    subtotal: Decimal
    shipping: Decimal
    total: Decimal
    payment_method: PaymentMethod
    status: OrderStatus
    items: list[OrderItemResponse]
