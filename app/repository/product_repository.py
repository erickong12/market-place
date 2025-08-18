from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from app.models.inventory import SellerInventory
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.repository.common import find_paginated
from typing import Optional

from app.schemas.common import Page
from app.utils.enums import OrderStatus


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Product

    def find_all(self) -> list[Product]:
        return self.db.query(self.model).filter(self.model.delete == False).all()

    def find_all_paginated(
        self, skip: int, limit: int, sort_by: str, order: str, search: Optional[str]
    ) -> Page:
        query = self.db.query(self.model).filter(self.model.delete == False)
        if search:
            query = query.filter(self.model.name.icontains(search))
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def find_by_id(self, product_id: str) -> Optional[Product]:
        return (
            self.db.query(self.model)
            .filter(self.model.id == product_id)
            .filter(self.model.delete == False)
            .first()
        )

    def find_top_products(self, limit: int):
        return (
            self.db.query(
                self.model.id.label("id"),
                self.model.name.label("name"),
                self.model.image.label("image"),
                func.sum(OrderItem.quantity).label("total_sold"),
            )
            .join(SellerInventory, SellerInventory.id == OrderItem.seller_inventory_id)
            .join(self.model, self.model.id == SellerInventory.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .filter(Order.status == OrderStatus.DONE)
            .filter(self.model.delete == False)
            .group_by(self.model.id, self.model.name, self.model.image)
            .order_by(desc("total_sold"))
            .limit(limit)
            .all()
        )

    def save(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.db.commit()
        return product

    def delete(self, product: Product) -> None:
        product.delete = True
        self.db.commit()
