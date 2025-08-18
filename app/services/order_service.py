from sqlalchemy.orm import Session
from app.core.exception import BusinessError
from app.models.user import User
from app.repository.inventory_repository import SellerInventoryRepository
from app.repository.order_item_repository import OrderItemRepository
from app.repository.order_repository import OrderRepository
from app.schemas.order import (
    OrderItemResponse,
    OrderPageResponse,
    OrderResponse,
    OrderStatus,
)

from app.utils import util
from app.utils.enums import RoleEnum


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderRepository(db)
        self.repo_order_item = OrderItemRepository(db)
        self.repo_seller_inventory = SellerInventoryRepository(db)

    def list_orders(self, page: int, size: int, sort_by: str, order: str, user: User):
        skip = (page - 1) * size
        limit = size
        if user.role == RoleEnum.SELLER:
            result = self.repo.find_orders_by_seller(
                skip, limit, sort_by, order, user.id
            )
        elif user.role == RoleEnum.BUYER:
            result = self.repo.find_orders_by_buyer(
                skip, limit, sort_by, order, user.id
            )
        return OrderPageResponse(
            page=page,
            size=size,
            skip=skip,
            total_record=result.total,
            result=result.data,
        )
    def get_order_history(self, user: User):
        if user.role == RoleEnum.SELLER:
            result = self.repo.find_orders_by_seller(0, 100, "created_at", "desc", user.id)
        elif user.role == RoleEnum.BUYER:
            result = self.repo.find_orders_by_buyer(0, 100, "created_at", "desc", user.id)
        return OrderPageResponse(
            page=1,
            size=100,
            skip=0,
            total_record=result.total,
            result=result.data,
        )

    def get_order_items(self, order_id: str) -> list[OrderItemResponse]:
        result = self.repo_order_item.find_orders_items(order_id)
        return [OrderItemResponse(**item.__dict__) for item in result]

    def update_order_status(
        self, order_id: str, new_status: OrderStatus, user: User | None
    ) -> OrderResponse:
        try:
            with self.db.begin():
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
                return OrderResponse(**updated_order.__dict__)

        except Exception:
            self.db.rollback()
            raise
