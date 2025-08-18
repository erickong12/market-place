from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.exception import BusinessError
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.repository.cart_repository import CartRepository
from app.repository.inventory_repository import SellerInventoryRepository
from app.repository.order_repository import OrderRepository
from app.schemas.cart import CartItemCreate, CartItemResponse


class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CartRepository(db)
        self.inventory_repo = SellerInventoryRepository(db)
        self.order_repo = OrderRepository(db)

    def list_cart(self, user_id: str) -> list[CartItemResponse]:
        items = self.repo.find_all(user_id)
        return [CartItemResponse(**item.__dict__) for item in items]

    def add_to_cart(self, user_id: str, item: CartItemCreate) -> JSONResponse:
        cart = CartItem(
            buyer_id=user_id,
            seller_inventory_id=item.seller_inventory_id,
            quantity=item.quantity,
        )
        self.repo.create_cart(cart)
        return JSONResponse(status_code=201)

    def update_cart_item(
        self, cart_item_id: str, quantity: int, user_id: str
    ) -> JSONResponse:
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

        return JSONResponse(status_code=204)
    
    def clear_cart(self, user_id: str) -> JSONResponse:
        self.repo.clear_cart(user_id)
        return JSONResponse(status_code=204)
    
    def delete_cart_item(self, cart_item_id: str, user_id: str) -> JSONResponse:
        cart_item = self.repo.get_by_id(cart_item_id)
        if not cart_item:
            raise BusinessError("Cart item not found")

        if cart_item.buyer_id != user_id:
            raise BusinessError("Unauthorized to delete this cart item")

        self.repo.delete_cart_item(cart_item)
        return JSONResponse(status_code=204)

    def checkout(self, user_id: str):
        try:
            with self.db.begin():
                items = self.repo.find_all(user_id)
                if not items:
                    raise BusinessError("Cart is empty")

                items_by_seller = {}

                for item in items:
                    inv = self.inventory_repo.get_by_id_for_update(
                        item.seller_inventory_id
                    )
                    if not inv:
                        raise BusinessError("Inventory not found")

                    if inv.quantity < item.quantity:
                        raise BusinessError("Stock not enough")

                    inv.quantity -= item.quantity

                    if inv.seller_id not in items_by_seller:
                        items_by_seller[inv.seller_id] = []

                    items_by_seller[inv.seller_id].append(
                        OrderItem(
                            seller_inventory_id=inv.id,
                            quantity=item.quantity,
                            price_at_purchase=inv.price,
                        )
                    )

                for seller_id, order_items in items_by_seller.items():
                    self.order_repo.create_order_with_items(
                        Order(
                            buyer_id=user_id,
                            seller_id=seller_id,
                            items=order_items,
                        )
                    )

                return JSONResponse(status_code=201)

        except Exception:
            self.db.rollback()
            raise
