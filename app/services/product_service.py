import os
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core.exception import BusinessError
from app.repository.product_repository import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductLandingPage,
    ProductOut,
    ProductPageResponse,
    ProductResponse,
    ProductUpdate,
)
from app.schemas.common import PageResponse


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductRepository(db)

    def get_paginated(
        self, page: int, size: int, sort_by: str, order: str, search: str | None = None
    ) -> ProductPageResponse:
        skip = (page - 1) * size
        limit = size
        result = self.repo.find_all_paginated(skip, limit, sort_by, order, search)
        return ProductPageResponse(
            page=PageResponse(
                page=page, size=size, offset=skip, total_record=result[1]
            ),
            result=result.data,
        )

    def list_products_dropdown(self) -> list[ProductOut]:
        result = self.repo.find_all()
        return [ProductOut](
            [ProductOut(**item.__dict__) for item in result]
        )

    def get_landing_page(self, limit: int) -> list[ProductLandingPage]:
        result = self.repo.find_top_products(limit)
        return [ProductLandingPage](
            [ProductLandingPage(**item.__dict__) for item in result]
        )

    def get_product_by_id(self, product_id: str) -> ProductResponse:
        # Check if record exists
        entity = self.repo.find_by_id(product_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        return ProductResponse(**entity.__dict__)

    async def insert_product(
        self, data: ProductCreate, image: UploadFile | None
    ) -> ProductResponse:
        # Save image
        file_path = os.path.join(UPLOAD_DIR, str(uuid4()))
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        data.image = f"/{file_path}"
        entity = self.repo.save(data)
        return ProductResponse(**entity.__dict__)

    async def update_product(
        self, data: ProductUpdate, image: UploadFile | None
    ) -> ProductResponse:
        # Check if record exists
        entity = self.repo.find_by_id(data.id)
        if entity is None:
            raise BusinessError("Record Not Found")
        # Remove old image if exists
        if entity.image and os.path.exists(entity.image):
            os.remove(entity.image)
        # Save new image
        file_path = os.path.join(UPLOAD_DIR, str(uuid4()))
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        data.image = f"/{file_path}"
        entity.name = data.name
        entity.description = data.description
        entity.image = data.image
        return ProductResponse(**self.repo.update(entity).__dict__)

    def delete_product(self, product_id: str) -> dict:
        # Check if record exists
        entity = self.repo.find_by_id(product_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        # Remove old image if exists
        if entity.image and os.path.exists(entity.image):
            os.remove(entity.image)
        self.repo.delete(entity)
        return {"message": "Product deleted successfully"}
