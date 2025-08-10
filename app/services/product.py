import os
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core import exception
from app.repository.product import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductPageResponse,
    ProductResponse,
    ProductUpdate,
)
from app.schemas.common import PageResponse


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductRepository(db)

    def get_product_paginated(
        self, page: int, size: int, sort_by: str, order: str, search: str | None = None
    ) -> ProductPageResponse:
        skip = (page - 1) * size
        limit = size
        result = self.repo.find_all_paginated_products(
            skip, limit, sort_by, order, search
        )
        return ProductPageResponse(
            page=PageResponse(
                page=page, size=size, offset=skip, total_record=result[1]
            ),
            result=result[0],
        )

    def get_product_by_id(self, product_id: str) -> ProductResponse:
        entity = self.repo.find_product_by_id(product_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        return ProductResponse(**entity.__dict__)

    async def insert_product(
        self, data: ProductCreate, image: UploadFile | None
    ) -> ProductResponse:
        if image is not None:
            file_path = os.path.join(UPLOAD_DIR, str(uuid4()))
            with open(file_path, "wb") as buffer:
                buffer.write(await image.read())
            data.image_url = f"/{file_path}"
        entity = self.repo.create_product(data)
        return ProductResponse(**entity.__dict__)

    async def update_product(
        self, data: ProductUpdate, image: UploadFile | None
    ) -> ProductResponse:
        entity = self.repo.find_product_by_id(data.id)
        if entity is None:
            raise BusinessError("Record Not Found")

        if image is not None:
            # Remove old image if exists
            if entity.image_url and os.path.exists(entity.image_url):
                os.remove(entity.image_url)

            file_path = os.path.join(UPLOAD_DIR, str(uuid4()))
            with open(file_path, "wb") as buffer:
                buffer.write(await image.read())
            data.image_url = f"/{file_path}"

        updated_entity = self.repo.update_product(entity, data)
        return ProductResponse(**updated_entity.__dict__)

    def delete_product(self, product_id: str) -> dict:
        entity = self.repo.find_product_by_id(product_id)
        if entity is None:
            raise BusinessError("Record Not Found")

        if entity.image_url and os.path.exists(entity.image_url):
            os.remove(entity.image_url)

        self.repo.delete_product_by_id(product_id)
        return {"message": "Product deleted successfully"}
