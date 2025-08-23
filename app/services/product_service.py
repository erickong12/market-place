import os
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.dependency import transactional
from app.core.exception import BusinessError
from app.models.product import Product
from app.repository.inventory_repository import SellerInventoryRepository
from app.repository.product_repository import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductLandingPage,
    ProductPageResponse,
    ProductResponse,
    ProductUpdate,
)
from app.utils import util


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductRepository(db)
        self.inventory_repo = SellerInventoryRepository(db)

    def get_paginated(
        self, page: int, size: int, sort_by: str, order: str, search: str | None = None
    ) -> ProductPageResponse:
        skip = (page - 1) * size
        limit = size
        result = self.repo.find_all_paginated(skip, limit, sort_by, order, search)
        return ProductPageResponse(
            page=page,
            size=size,
            skip=skip,
            total_record=result.total,
            result=result.data,
        )

    def get_landing_page(self, limit: int) -> list[ProductLandingPage]:
        result = self.repo.find_top_products(limit)
        return [ProductLandingPage(**item._mapping) for item in result]

    def get_product_by_id(self, product_id: str) -> ProductResponse:
        entity = self.repo.find_by_id(product_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        return ProductResponse(**entity.__dict__)

    @transactional
    async def insert_product(self, data: ProductCreate, image: UploadFile):
        image_url = await util.save_upload_file(image)
        product = Product(
            name=data.name,
            description=data.description,
            image=image_url
        )
        self.repo.save(product)
        return JSONResponse(status_code=201, content={"detail": "Product created"})


    @transactional
    async def update_product(self, data: ProductUpdate, image: UploadFile | None):
        entity = self.repo.find_by_id(data.id)
        if entity is None:
            raise BusinessError("Record Not Found")

        if image:
            util.delete_file(entity.image)
            entity.image = await util.save_upload_file(image)

        entity.name = data.name
        entity.description = data.description
        self.repo.update(entity)
        return JSONResponse(status_code=200, content={"detail": "Product updated"})

    @transactional
    def delete_product(self, product_id: str):
        entity = self.repo.find_by_id(product_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        if entity.image and os.path.exists(entity.image):
            os.remove(entity.image)
        self.repo.delete(entity)
        self.inventory_repo.delete_by_product_id(product_id)
        return JSONResponse(status_code=200, content={"detail": "Product deleted"})
