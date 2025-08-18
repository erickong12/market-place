from sqlalchemy import not_
from sqlalchemy.orm import Session, joinedload
from app.models.order import Order
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
        query = (
            self.db.query(
                self.model.id,
                User.name.label("buyer_id"),
                User.name.label("buyer_name"),
                User.name.label("seller_id"),
                User.name.label("seller_name"),
                self.model.status,
                self.model.created_at,
                self.model.updated_at,
            )
            .join(User, User.id == self.model.buyer_id)
            .join(User, User.id == self.model.seller_id)
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
        )
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def find_orders_by_buyer(
        self, skip: int, limit: int, sort_by: str, order: str, buyer_id: str
    ) -> Page:
        query = (
            self.db.query(
                self.model.id,
                User.name.label("buyer_id"),
                User.name.label("buyer_name"),
                User.name.label("seller_id"),
                User.name.label("seller_name"),
                self.model.status,
                self.model.created_at,
                self.model.updated_at,
            )
            .join(User, User.id == self.model.buyer_id)
            .join(User, User.id == self.model.seller_id)
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

    def create_order_with_items(self, order: Order):
        self.db.add(order)
        self.db.commit()
        return order

    def update_order_status(self, order: Order, new_status: OrderStatus):
        order.status = new_status.value
        self.db.commit()
        return order
