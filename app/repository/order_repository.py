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

    def __build_order_query(self, party: str, party_id: str, history: bool):
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
            .filter(getattr(self.model, f"{party}_id") == party_id)
        )

        status_filter = [
            OrderStatus.DONE,
            OrderStatus.CANCELLED,
            OrderStatus.AUTO_CANCELLED,
        ]

        if history:
            query = query.filter(self.model.status.in_(status_filter))
        else:
            query = query.filter(not_(self.model.status.in_(status_filter)))

        return query.group_by(
            self.model.id,
            buyer.name,
            seller.name,
            self.model.status,
            self.model.created_at,
            self.model.updated_at,
        )

    def find_orders_by_seller(
        self,
        skip: int,
        limit: int,
        sort_by: str,
        order: str,
        seller_id: str,
        history: bool = False,
    ) -> Page:
        query = self.__build_order_query("seller", seller_id, history)
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def find_orders_by_buyer(
        self,
        skip: int,
        limit: int,
        sort_by: str,
        order: str,
        buyer_id: str,
        history: bool = False,
    ) -> Page:
        query = self.__build_order_query("buyer", buyer_id, history)
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
