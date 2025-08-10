from sqlalchemy.orm import Session
from app.models.product import Product
from app.repository.common import find_all_paginated
from app.schemas.product import ProductCreate, ProductUpdate
from typing import Optional, Tuple, List


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all_paginated_products(
        self,
        skip: int,
        limit: int,
        sort_by: str,
        order: str,
        search: Optional[str] = None,
    ) -> Tuple[List[Product], int]:
        query = self.db.query(Product)
        if search:
            query = query.filter(Product.name.icontains(search))
        return find_all_paginated(query, Product, skip, limit, sort_by, order)

    def find_product_by_id(self, product_id: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create_product(self, product_data: ProductCreate) -> Product:
        db_product = Product(**product_data.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update_product(self, product: Product, product_data: ProductUpdate) -> Product:
        product.name = product_data.name
        product.description = product_data.description
        product.image = product_data.image
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product_by_id(self, product_id: str) -> None:
        self.db.query(Product).filter(Product.id == product_id).delete()
        self.db.commit()
