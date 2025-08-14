from sqlalchemy.orm import Session
from app.core.exception import BusinessError
from app.models.order import Order
from app.repository.inventory_repository import SellerInventoryRepository
from app.repository.order_repository import OrderRepository
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatus,
)
from typing import List

from app.utils import util


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderRepository(db)
        self.repo_seller_inventory = SellerInventoryRepository(db)

    def create_order(self, buyer_id: str, order_data: OrderCreate) -> OrderResponse:
        # Could add validation: check stock, seller exists, etc.
        for item in order_data.items:
            seller_inventory = (
                self.repo_seller_inventory.get_inventory_by_product_and_seller(
                    item.product_id, order_data.seller_id
                )
            )
            if seller_inventory is None:
                raise BusinessError("Record Not Found")
            if seller_inventory.quantity < item.quantity:
                raise BusinessError("Not enough stock for")
        order = self.repo.create_order(buyer_id, order_data)
        return self._map_order_to_response(order)

    def get_orders_by_buyer(self, buyer_id: str) -> List[OrderResponse]:
        orders = self.repo.get_orders_by_buyer(buyer_id)
        return [self._map_order_to_response(o) for o in orders]

    def get_orders_by_seller(self, seller_id: str) -> List[OrderResponse]:
        orders = self.repo.get_orders_by_seller(seller_id)
        return [self._map_order_to_response(o) for o in orders]

    def update_order_status(
        self, order_id: str, new_status: OrderStatus, user_id: str
    ) -> OrderResponse:
        order = self.repo.get_order_by_id(order_id)
        if order is None:
            raise BusinessError("Record Not Found")
        if order.buyer_id != user_id and order.seller_id != user_id:
            raise BusinessError("Unauthorized to update this order")

        # Validate allowed transitions (simple example)
        if not util.valid_status_transition(order.status, new_status.value):
            raise BusinessError("Invalid order status transition")

        updated_order = self.repo.update_order_status(order, new_status)
        return self._map_order_to_response(updated_order)

    def _map_order_to_response(self, order: Order) -> OrderResponse:
        # Map ORM order + items to Pydantic response
        return OrderResponse(
            id=order.id,
            buyer_id=order.buyer_id,
            seller_id=order.seller_id,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                }
                for item in order.items
            ],
        )
