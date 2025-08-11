from sqlalchemy import desc, func
from sqlalchemy.orm import Session, joinedload
from app.models.inventory import SellerInventory
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderStatus
from typing import List, Optional


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order_with_items(self, buyer_id: str, seller_id: str, items_data: list):
        order = Order(buyer_id=buyer_id, seller_id=seller_id)
        self.db.add(order)
        self.db.flush()

        for item in items_data:
            self.db.add(
                OrderItem(
                    order_id=order.id,
                    seller_inventory_id=item["seller_inventory_id"],
                    quantity=item["quantity"],
                    price_at_purchase=item["price_at_purchase"],
                )
            )

        self.db.flush()
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
        self.db.refresh(order)
        return order

    def get_top_products(db: Session, limit: int):
        return (
            db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(OrderItem.quantity).label("total_sold"),
            )
            .join(SellerInventory, SellerInventory.id == OrderItem.seller_inventory_id)
            .join(Product, Product.id == SellerInventory.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .filter(Order.status == OrderStatus.DONE)
            .group_by(Product.id, Product.name)
            .order_by(desc("total_sold"))
            .limit(limit)
            .all()
        )

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
