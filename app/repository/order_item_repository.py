from sqlalchemy.orm import Session
from app.models.inventory import SellerInventory
from app.models.order import OrderItem
from app.models.product import Product


class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = OrderItem

    def find_orders_items(self, order_id: str):
        return (
            self.db.query(
                self.model.id,
                self.model.quantity,
                self.model.price_at_purchase,
                Product.name.label("product_name"),
                Product.image.label("product_image"),
                Product.description.label("product_description"),
            )
            .join(SellerInventory, SellerInventory.id == self.model.seller_inventory_id)
            .join(Product, Product.id == SellerInventory.product_id)
            .filter(self.model.order_id == order_id)
            .all()
        )
