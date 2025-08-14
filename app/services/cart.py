# app/service/checkout_service.py
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.repository.inventory_repository import SellerInventoryRepository
from app.repository.order_repository import OrderRepository
from app.repository.order_item import OrderItemRepository
from app.schemas.order import OrderCreate, OrderItemCreate

class CheckoutService:
    """
    Service handling the checkout process for a marketplace.

    Ensures:
    - Inventory is locked and stock is reduced atomically
    - Orders and order items are persisted in a single transaction
    - Insufficient stock results in rollback
    """

    def __init__(self, db: Session):
        self.db = db
        self.inventory_repo = SellerInventoryRepository(db)
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)

    def checkout(self, user_id: str, items: List[OrderItemCreate]) -> dict:
        try:
            # Begin transaction
            with self.db.begin():
                total_amount = 0
                order_items_to_create = []

                for item in items:
                    inv = self.inventory_repo.get_inventory_by_id(item.inventory_id)
                    if not inv:
                        raise HTTPException(status_code=404, detail=f"Inventory {item.inventory_id} not found")

                    if inv.stock < item.quantity:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Insufficient stock for product {inv.product_id} from seller {inv.seller_id}"
                        )

                    # Reduce stock
                    inv.stock -= item.quantity
                    total_amount += inv.price * item.quantity

                    # Prepare order item
                    order_items_to_create.append({
                        "product_id": inv.product_id,
                        "inventory_id": inv.id,
                        "seller_id": inv.seller_id,
                        "quantity": item.quantity,
                        "price": inv.price
                    })

                # Create order
                order_data = OrderCreate(
                    user_id=user_id,
                    total_amount=total_amount,
                    status="PENDING"
                )
                order = self.order_repo.create_order_with_items(user_id, order_data, order_items_to_create)

                # Create order items
                for oi in order_items_to_create:
                    order_item_data = OrderItemCreate(
                        order_id=order.id,
                        **oi
                    )
                    self.order_item_repo.create_order_item(order_item_data)

                return {
                    "order_id": order.id,
                    "total_amount": total_amount,
                    "status": order.status
                }

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error during checkout")
