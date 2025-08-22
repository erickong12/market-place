from sqlalchemy import func, not_
from sqlalchemy.orm import Session, joinedload, aliased
from app.models.order import Order, OrderItem
from app.models.user import User
from app.repository.common import find_paginated
from app.schemas.common import Page
from app.schemas.order import OrderStatus
from typing import Optional


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Order

    def find_orders_by_seller(
        self, skip: int, limit: int, sort_by: str, order: str, seller_id: str
    ) -> Page:
        buyer = aliased(User)
        seller = aliased(User)
        query = (
            self.db.query(
                self.model.id,
                buyer.name.label("buyer_id"),
                buyer.name.label("buyer_name"),
                seller.name.label("seller_id"),
                seller.name.label("seller_name"),
                self.model.status,
                self.model.created_at,
                self.model.updated_at,
                func.sum(OrderItem.quantity * OrderItem.price_at_purchase).label(
                    "total"
                ),
            )
            .join(buyer, buyer.id == Order.buyer_id)
            .join(seller, seller.id == Order.seller_id)
            .join(OrderItem, OrderItem.order_id == self.model.id)
            .filter(self.model.seller_id == seller_id)
            .filter(
                not_(
                    self.model.status.in_(
                        [
                            OrderStatus.DONE,
                            OrderStatus.CANCELLED,
                            OrderStatus.AUTO_CANCELLED,
                        ]
                    )
                )
            )
            .group_by(
                self.model.id,
                buyer.name,
                seller.name,
                self.model.status,
                self.model.created_at,
                self.model.updated_at,
            )
        )
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def find_orders_by_buyer(
        self, skip: int, limit: int, sort_by: str, order: str, buyer_id: str
    ) -> Page:
        buyer = aliased(User)
        seller = aliased(User)
        query = (
            self.db.query(
                self.model.id,
                buyer.name.label("buyer_id"),
                buyer.name.label("buyer_name"),
                seller.name.label("seller_id"),
                seller.name.label("seller_name"),
                self.model.status,
                self.model.created_at,
                self.model.updated_at,
                func.sum(OrderItem.quantity * OrderItem.price_at_purchase).label(
                    "total"
                ),
            )
            .join(buyer, buyer.id == Order.buyer_id)
            .join(seller, seller.id == Order.seller_id)
            .join(OrderItem, OrderItem.order_id == self.model.id)
            .filter(self.model.buyer_id == buyer_id)
            .filter(
                not_(
                    self.model.status.in_(
                        [
                            OrderStatus.DONE,
                            OrderStatus.CANCELLED,
                            OrderStatus.AUTO_CANCELLED,
                        ]
                    )
                )
            ).group_by(
                self.model.id,
                buyer.name,
                seller.name,
                self.model.status,
                self.model.created_at,
                self.model.updated_at,
            )
        )
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        return (
            self.db.query(self.model)
            .filter(self.model.id == order_id)
            .options(joinedload(self.model.items))
            .first()
        )

    def create_order_with_items(self, order: list[Order]):
        self.db.add_all(order)

    def update_order_status(self, order: Order, new_status: OrderStatus):
        order.status = new_status.value
        self.db.add(order)
        return order
