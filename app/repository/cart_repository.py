from app.models.cart import CartItem
from sqlalchemy.orm import Session

from app.models.inventory import SellerInventory

from app.models.product import Product
from app.models.user import User


class CartRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = CartItem

    def find_all(self, buyer_id: str):
        return (
            self.db.query(
                CartItem.id,
                CartItem.quantity,
                SellerInventory.id.label("inventory_id"),
                SellerInventory.price,
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.image,
                User.id.label("seller_id"),
                User.name.label("seller_name"),
            )
            .join(CartItem.seller_inventory)
            .join(SellerInventory.product)
            .join(SellerInventory.seller)
            .filter(self.model.buyer_id == buyer_id)
            .all()
        )

    def get_by_id(self, cart_id):
        return self.db.query(self.model).filter_by(id=cart_id).first()

    def get_by_buyer_id_and_inventory_id(self, buyer_id, inventory_id):
        return (
            self.db.query(self.model)
            .filter_by(buyer_id=buyer_id, seller_inventory_id=inventory_id)
            .first()
        )

    def create_cart(self, cart: CartItem):
        self.db.add(cart)
        return cart

    def update_cart(self, cart: CartItem):
        self.db.add(cart)

    def delete_cart_item(self, cart_item: CartItem):
        self.db.delete(cart_item)

    def clear_cart(self, buyer_id: str):
        self.db.query(CartItem).filter(CartItem.buyer_id == buyer_id).delete()
