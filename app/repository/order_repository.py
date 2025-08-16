from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.order import OrderStatus
from typing import List, Optional


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order_with_items(self, order: Order):
        self.db.add(order)
        self.db.commit()
        return order

    def get_orders_by_buyer(self, buyer_id: str) -> List[Order]:
        return (
            self.db.query(Order)
            .filter(Order.buyer_id == buyer_id)
            .options(joinedload(Order.items))
            .order_by(Order.created_at.desc())
            .all()
        )

    def get_orders_by_seller(self, seller_id: str) -> List[Order]:
        return (
            self.db.query(Order)
            .filter(Order.seller_id == seller_id)
            .options(joinedload(Order.items))
            .order_by(Order.created_at.desc())
            .all()
        )

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        return (
            self.db.query(Order)
            .filter(Order.id == order_id)
            .options(joinedload(Order.items))
            .first()
        )

    def update_order_status(self, order: Order, new_status: OrderStatus):
        order.status = new_status.value
        self.db.commit()
        return order

    def get_top_sellers(db: Session, limit: int):
        return (
            db.query(
                User.id.label("seller_id"),
                User.username.label("seller_name"),
                OrderItem.quantity.label("total_sales"),
            )
            .join(Order, Order.id == OrderItem.order_id)
            .join(User, User.id == Order.seller_id)
            .filter(Order.status == OrderStatus.COMPLETED)
            .group_by(User.id, User.username)
            .order_by(desc("total_sales"))
            .limit(limit)
            .all()
        )
