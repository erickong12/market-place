from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.dependency import transactional
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
        return [CartItemResponse(**item._mapping) for item in items]

    @transactional
    def add_to_cart(self, user_id: str, item: CartItemCreate) -> JSONResponse:
        entity = self.repo.get_by_buyer_id_and_inventory_id(
            user_id, item.seller_inventory_id
        )
        if entity:
            entity.quantity += item.quantity
            self.repo.update_cart(entity)
        else:
            cart = CartItem(
                buyer_id=user_id,
                seller_inventory_id=item.seller_inventory_id,
                quantity=item.quantity,
            )
            self.repo.create_cart(cart)
        return JSONResponse(status_code=201, content={"detail": "Item added to cart"})

    @transactional
    def update_cart_item(
        self, cart_item_id: str, quantity: int, user_id: str
    ) -> JSONResponse:
        cart_item = self.repo.get_by_id(cart_item_id)
        if not cart_item:
            raise BusinessError("Cart item not found")

        if cart_item.buyer_id != user_id:
            raise BusinessError("Unauthorized to update this cart item")

        if quantity <= 0:
            self.repo.delete_cart_item(cart_item)
        else:
            cart_item.quantity = quantity
            self.repo.update_cart(cart_item)

        return JSONResponse(status_code=200, content={"detail": "Cart item updated"})

    @transactional
    def clear_cart(self, user_id: str) -> JSONResponse:
        self.repo.clear_cart(user_id)
        return JSONResponse(status_code=200, content={"detail": "Cart cleared"})

    @transactional
    def delete_cart_item(self, cart_item_id: str, user_id: str) -> JSONResponse:
        cart_item = self.repo.get_by_id(cart_item_id)
        if not cart_item:
            raise BusinessError("Cart item not found")

        if cart_item.buyer_id != user_id:
            raise BusinessError("Unauthorized to delete this cart item")

        self.repo.delete_cart_item(cart_item)
        return JSONResponse(status_code=200, content={"detail": "Cart item deleted"})

    @transactional
    def checkout(self, user_id: str):
        items = self.repo.find_all(user_id)
        if not items:
            raise BusinessError("Cart is empty")

        orders_by_seller = {}

        for item in items:
            inv = self.inventory_repo.get_by_id_for_update(item.inventory_id)
            if not inv:
                raise BusinessError("Inventory not found")

            if inv.quantity < item.quantity:
                raise BusinessError("Stock not enough")

            inv.quantity -= item.quantity

            if inv.seller_id not in orders_by_seller:
                orders_by_seller[inv.seller_id] = Order(
                    buyer_id=user_id, seller_id=inv.seller_id, items=[]
                )

            orders_by_seller[inv.seller_id].items.append(
                OrderItem(
                    seller_inventory_id=inv.id,
                    quantity=item.quantity,
                    price_at_purchase=inv.price,
                )
            )

        self.order_repo.create_order_with_items(list(orders_by_seller.values()))
        self.repo.clear_cart(user_id)

        return JSONResponse(status_code=201, content={"detail": "Order created"})
