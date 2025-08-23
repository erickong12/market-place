from pydantic import BaseModel, ConfigDict, Field
from typing import List
from datetime import datetime
from app.utils.enums import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)
    price_at_purchase: float


class OrderCreate(BaseModel):
    seller_id: str
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: str
    product_name: str
    product_image: str
    product_description: str
    quantity: int
    price_at_purchase: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: str
    buyer_id: str
    buyer_name: str
    seller_id: str
    seller_name: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    total: float

    model_config = ConfigDict(from_attributes=True)


class OrderPageResponse(BaseModel):
    page: int
    size: int
    skip: int
    total_record: int
    result: list[OrderResponse]
