from sqlalchemy.orm import Session
from app.core.exception import BusinessError
from app.models.user import User
from app.repository.inventory_repository import SellerInventoryRepository
from app.repository.order_repository import OrderRepository
from app.schemas.order import (
    OrderResponse,
    OrderStatus,
)
from typing import List

from app.utils import util
from app.utils.enums import RoleEnum


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderRepository(db)
        self.repo_seller_inventory = SellerInventoryRepository(db)

    def get_orders_by_buyer(self, buyer_id: str) -> List[OrderResponse]:
        orders = self.repo.get_orders_by_buyer(buyer_id)
        return [self._map_order_to_response(o) for o in orders]

    def get_orders_by_seller(self, seller_id: str) -> List[OrderResponse]:
        orders = self.repo.get_orders_by_seller(seller_id)
        return [self._map_order_to_response(o) for o in orders]

    def update_order_status(
        self, order_id: str, new_status: OrderStatus, user: User | None
    ) -> OrderResponse:
        order = self.repo.get_order_by_id(order_id)
        if order is None:
            raise BusinessError("Record Not Found")

        if not util.valid_status_transition(order.status, new_status.value):
            raise BusinessError("Invalid order status transition")
        if user:
            if order.seller_id != user.id and user.role != RoleEnum.SELLER:
                raise BusinessError("Unauthorized to update this order")
            elif order.buyer_id != user.id and user.role != RoleEnum.BUYER:
                raise BusinessError("Unauthorized to update this order")

        updated_order = self.repo.update_order_status(order, new_status)

        if (
            new_status == OrderStatus.CANCELLED
            or new_status == OrderStatus.AUTO_CANCELLED
        ):
            for item in updated_order.items:
                inv = self.repo_seller_inventory.get_by_id_for_update(
                    item.seller_inventory_id
                )
                if inv is None:
                    raise BusinessError("Inventory not found")
                inv.quantity += item.quantity
                self.repo_seller_inventory.update(inv)
        return self._map_order_to_response(updated_order)
