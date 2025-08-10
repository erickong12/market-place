import os
from uuid import uuid4
from fastapi import UploadFile
from requests import Session

from app.core.config import UPLOAD_DIR
from app.core import exception
from app.repository import product
from app.schemas.product import (
    ProductCreate,
    ProductPageResponse,
    ProductResponse,
    ProductUpdate,
)
from app.schemas.common import PageResponse


def get_product_paginated(
    db: Session, page: int, size: int, sort_by: str, order: str, search: str | None
):
    skip = (page - 1) * size
    limit = size
    result = product.find_all_paginated_products(
        db, skip, limit, sort_by, order, search
    )
    return ProductPageResponse(
        page=PageResponse(page=page, size=size, offset=skip, total_record=result.total),
        result=result.data,
    )


def get_product_by_id(db: Session, product_id: str):
    entity = product.find_product_by_id(product_id, db)
    if product is None:
        raise exception.RECORD_NOT_FOUND
    return ProductResponse(**entity.__dict__)


async def insert_product(db: Session, data: ProductCreate, image: UploadFile):
    if image is not None:
        file_path = os.path.join(UPLOAD_DIR, uuid4())
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        data.image = f"/{file_path}"
    return ProductResponse(**product.create_product(db, data).__dict__)


async def update_product(db: Session, data: ProductUpdate, image: UploadFile):
    entity = product.find_product_by_id(db, data.id)
    if entity is None:
        raise exception.RECORD_NOT_FOUND
    if image is not None:
        if entity.image is not None:
            if os.path.exists(entity.image):
                os.remove(entity.image)
        file_path = os.path.join(UPLOAD_DIR, uuid4())
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        data.image = f"/{file_path}"
    return ProductResponse(**product.update_product(db, entity, data).__dict__)


def delete_product(db: Session, product_id: str):
    entity = product.find_product_by_id(db, product_id)
    if entity is None:
        raise exception.RECORD_NOT_FOUND
    if entity.image is not None:
        if os.path.exists(entity.image):
            os.remove(entity.image)
    product.delete_product_by_id(db, product_id)
    return {"message": "Product deleted successfully"}
