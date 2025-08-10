from sqlalchemy.orm import Session, joinedload
from app.core import exception
from app.models.inventory import SellerInventory
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderStatus
from typing import List, Optional
from datetime import datetime
from uuid import uuid4


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, buyer_id: str, order_data: OrderCreate) -> Order:
        order = Order(
            id=str(uuid4()),
            buyer_id=buyer_id,
            seller_id=order_data.seller_id,
            status=OrderStatus.PENDING.value,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(order)
        self.db.flush()  # to get order.id if needed

        # Create order items
        for item in order_data.items:
            order_item = OrderItem(
                id=str(uuid4()),
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                # Assuming price is fetched here (should query product price)
                price=self._get_product_price(item.product_id, order_data.seller_id),
            )
            self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order)
        return order

    def _get_product_price(self, product_id: str, seller_id: str) -> float:
        # Query product price from SellerInventory
        product_inventory = (
            self.db.query(SellerInventory)
            .filter(SellerInventory.product_id == product_id)
            .filter(SellerInventory.seller_id == seller_id)
            .first()
        )
        if product_inventory is None:
            raise BusinessError("Record Not Found")
        return product_inventory.price

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
        order.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(order)
        return order
