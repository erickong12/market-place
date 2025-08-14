# app/repository/inventory.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.inventory import SellerInventory
from app.models.product import Product
from app.models.user import User
from app.repository.common import find_paginated


class SellerInventoryRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = SellerInventory

    def get_inventory_list(
        self,
        skip: int,
        limit: int,
        sort_by: str,
        order: str,
        search: str | None,
        seller_id: str | None,
    ) -> List[SellerInventory]:
        query = (
            self.db.query(
                self.model.id.label("id"),
                self.model.product_id.label("product_id"),
                self.model.quantity.label("quantity"),
                self.model.price.label("price"),
                Product.name.label("product_name"),
                Product.image.label("product_image"),
                Product.description.label("product_description"),
                User.id.label("seller_id"),
                User.name.label("seller_name"),
            )
            .join(Product, Product.id == self.model.product_id)
            .join(User, User.id == self.model.seller_id)
        )

        if seller_id is not None:
            query = query.filter(self.model.seller_id == seller_id)
        if search is not None:
            query = query.filter(Product.name.icontains(search))
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def get_inventory_by_id(self, inv_id: str) -> Optional[SellerInventory]:
        return self.db.query(self.model).filter(self.model.id == inv_id).first()

    def create(self, entity: SellerInventory):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: SellerInventory) -> SellerInventory:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_inventory(self, entity: SellerInventory):
        entity.delete = True
        self.db.commit()
