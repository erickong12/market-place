from sqlalchemy.orm import Session
from app.models.product import Product
from app.repository.common import find_paginated
from typing import Optional

from app.schemas.common import Page


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Product

    def find_all_paginated(
        self, skip: int, limit: int, sort_by: str, order: str, search: Optional[str]
    ) -> Page:
        query = self.db.query(self.model)
        if search:
            query = query.filter(self.model.name.icontains(search))
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def find_by_id(self, product_id: str) -> Optional[Product]:
        return self.db.query(self.model).filter(self.model.id == product_id).first()

    def find_top_products(
        self, skip: int, limit: int, sort_by: str, order: str
    ) -> Page:
        query = self.db.query(self.model).filter(self.model.delete == False)
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def save(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        product.delete = True
        self.db.commit()
