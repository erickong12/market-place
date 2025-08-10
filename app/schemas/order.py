from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.utils.enums import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    seller_id: str
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: str
    quantity: int
    price: float  # price at the time of order


class OrderResponse(BaseModel):
    id: str
    buyer_id: str
    seller_id: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
