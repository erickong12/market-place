from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from requests import Session

from app.core import exception
from app.core.exception import UnauthorizedUserException
from app.models.cart import CartItem
from app.models.order import Order, OrderItem, OrderStatus
from app.services import inventory


def get_orders(buyer_id: int, db: Session):
    return db.query(Order).filter(Order.buyer_id == buyer_id).all()


def get_order_by_id(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise exception.RECORD_NOT_FOUND
    return order


def checkout_order(buyer_id: int, db: Session):
    cart_items = db.query(CartItem).filter(CartItem.buyer_id == buyer_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    seller_ids = {item.seller_inventory.seller_id for item in cart_items}
    if len(seller_ids) != 1:
        raise UnauthorizedUserException()
    seller_id = seller_ids.pop()

    try:
        order = Order(
            buyer_id=buyer_id,
            seller_id=seller_id,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(order)
        db.flush()

        for item in cart_items:
            inv = inventory.get_inventory_by_id(db, item.seller_inventory_id)

            if not inv or inv.quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock for item {inv.product_id}",
                )

            inv.quantity -= item.quantity
            db.add(
                OrderItem(
                    order_id=order.id,
                    seller_inventory_id=item.seller_inventory_id,
                    quantity=item.quantity,
                    price_at_purchase=inv.price,
                )
            )

        db.query(CartItem).filter(CartItem.buyer_id == buyer_id).delete()
        db.commit()
        db.refresh(order)
        return order
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
