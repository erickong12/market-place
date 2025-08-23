# app/repository/inventory.py
from typing import Optional
from sqlalchemy.orm import Session
from app.models.inventory import SellerInventory
from app.models.product import Product
from app.models.user import User
from app.repository.common import find_paginated
from app.schemas.common import Page


class SellerInventoryRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = SellerInventory

    def find_all_pagination(
        self,
        skip: int,
        limit: int,
        sort_by: str,
        order: str,
        search: str | None,
        seller_id: str | None,
    ) -> Page:
        query = (
            self.db.query(
                self.model.id,
                self.model.quantity,
                self.model.price,
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.image.label("product_image"),
                Product.description.label("product_description"),
                User.id.label("seller_id"),
                User.name.label("seller_name"),
            )
            .join(Product.inventory)
            .join(SellerInventory.seller)
            .filter(self.model.delete == False)
        )

        if seller_id:
            query = query.filter(self.model.seller_id == seller_id)
        if search:
            query = query.filter(Product.name.icontains(search))
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def get_by_id(self, inv_id: str) -> Optional[SellerInventory]:
        return self.db.query(self.model).filter(self.model.id == inv_id).first()

    def get_by_id_for_update(self, inv_id: str) -> Optional[SellerInventory]:
        return (
            self.db.query(self.model)
            .filter(self.model.id == inv_id)
            .with_for_update()
            .first()
        )
    def get_by_product_and_seller_for_update(self, seller_id: str, product_id: str) -> Optional[SellerInventory]:
        return (
            self.db.query(self.model)
            .filter(self.model.seller_id == seller_id, self.model.product_id == product_id)
            .with_for_update()
            .first()
        )

    def create(self, entity: SellerInventory) -> SellerInventory:
        self.db.add(entity)

    def update(self, entity: SellerInventory) -> SellerInventory:
        self.db.add(entity)

    def delete(self, entity: SellerInventory) -> None:
        entity.delete = True

    def delete_by_product_id(self, product_id: str) -> None:
        self.db.query(self.model).filter(self.model.product_id == product_id).update({"delete": True})
