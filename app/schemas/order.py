from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.order import OrderStatus
from app.schemas.common import PageResponse
from app.schemas.inventory import SellerInventoryResponse
from app.schemas.user import UserOut


class OrderItemCreate(BaseModel):
    seller_inventory_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    inventory: SellerInventoryResponse
    quantity: int
    price_at_purchase: float

    model_config = ConfigDict(from_attributes=True)


class OrderDetail(BaseModel):
    id: int
    buyer: UserOut
    seller: UserOut
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderPageResponse(BaseModel):
    data: list[OrderResponse]
    page: PageResponse
