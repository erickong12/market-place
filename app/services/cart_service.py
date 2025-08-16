from typing import List
from fastapi import Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exception import BusinessError
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.repository.cart_repository import CartRepository
from app.repository.inventory_repository import SellerInventoryRepository
from app.repository.order_repository import OrderRepository
from app.schemas.cart import CartItemCreate
from app.schemas.order import OrderItemCreate


class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CartRepository(db)
        self.inventory_repo = SellerInventoryRepository(db)
        self.order_repo = OrderRepository(db)

    def list_cart(self, user_id: str) -> List[OrderItemCreate]:
        items = self.repo.find_all(user_id)
        return items

    def add_to_cart(self, user_id: str, item: CartItemCreate) -> Response:
        cart = CartItem(
            buyer_id=user_id,
            seller_inventory_id=item.seller_inventory_id,
            quantity=item.quantity,
        )
        self.repo.create_cart(cart)
        return Response(status_code=201)

    def update_cart_item(
        self, cart_item_id: str, quantity: int, user_id: str
    ) -> Response:
        cart_item = self.repo.get_by_id(cart_item_id)
        if not cart_item:
            raise BusinessError("Cart item not found")

        if cart_item.buyer_id != user_id:
            raise BusinessError("Unauthorized to update this cart item")

        if quantity <= 0:
            self.repo.delete_cart_item(cart_item_id)
        else:
            cart_item.quantity = quantity
            self.repo.update_cart(cart_item)

        return Response(status_code=204)

    def checkout(self, user_id: str) -> dict:
        try:
            with self.db.begin():
                order_items_to_create = [OrderItem]
                items = self.repo.find_all(user_id)
                for item in items:
                    inv = self.inventory_repo.get_by_id_for_update(
                        item.seller_inventory_id
                    )
                    if not inv:
                        raise BusinessError("Inventory not found")

                    if inv.quantity < item.quantity:
                        raise BusinessError("stock not enough")

                    inv.quantity -= item.quantity
                    order_items_to_create.append(
                        OrderItem(
                            seller_inventory_id=inv.id,
                            quantity=item.quantity,
                            price_at_purchase=inv.price,
                        )
                    )

                self.order_repo.create_order_with_items(
                    Order(
                        buyer_id=user_id,
                        seller_id=inv.seller_id,
                        items=order_items_to_create,
                    )
                )

                return Response(status_code=201)

        except IntegrityError as e:
            self.db.rollback()
            raise
