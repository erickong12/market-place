from requests import Session

from app.models.product import Product
from app.repository.common import find_all_paginated
from app.schemas.product import ProductCreate, ProductUpdate


def find_all_paginated_products(
    db: Session, skip: int, limit: int, sort_by: str, order: str, search: str | None
):
    query = db.query(Product)
    if search is not None:
        query = query.filter(Product.name.ilike(search))
    return find_all_paginated(query, Product, skip, limit, sort_by, order)


def find_product_by_id(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product: Product, product_data: ProductUpdate):
    product.name = product_data.name
    product.description = product_data.description
    product.image = product_data.image
    db.commit()
    db.refresh(product)
    return product


def delete_product_by_id(db: Session, product_id: str):
    db.query(Product).filter(Product.id == product_id).delete()
    db.commit()
