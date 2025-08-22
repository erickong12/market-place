from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.dependency import transactional
from app.core.exception import BusinessError
from app.models.inventory import SellerInventory
from app.repository.inventory_repository import SellerInventoryRepository
from app.repository.product_repository import ProductRepository
from app.schemas.inventory import (
    SellerInventoryCreate,
    SellerInventoryPageResponse,
    SellerInventoryResponse,
    SellerInventoryUpdate,
)
from app.schemas.product import ProductDropListResponse


class SellerInventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SellerInventoryRepository(db)
        self.product_repo = ProductRepository(db)

    def list_all_inventory(
        self,
        page: int,
        size: int,
        sort_by: str,
        order: str,
        search: str | None,
        seller_id: str | None = None,
    ) -> SellerInventoryPageResponse:
        skip = (page - 1) * size
        limit = size
        entities = self.repo.find_all_pagination(
            skip, limit, sort_by, order, search, seller_id
        )
        return SellerInventoryPageResponse(
            page=page,
            size=size,
            skip=skip,
            total_record=entities.total,
            result=entities.data,
        )

    def get_product_list(self) -> list[ProductDropListResponse]:
        entities = self.product_repo.find_all()
        return [ProductDropListResponse(**entity._mapping) for entity in entities]

    def get_inventory(self, inventory_id: str) -> SellerInventoryResponse:
        entity = self.repo.get_by_id(inventory_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        return SellerInventoryResponse(**entity.__dict__)

    @transactional
    def add_inventory(
        self, data: SellerInventoryCreate, seller_id: str
    ) -> SellerInventoryResponse:
        entity = self.repo.get_by_product_and_seller_for_update(seller_id, data.product_id)
        if entity:
            entity.quantity = data.quantity
            entity.price = data.price
            self.repo.update(entity)
        else:
            entity = SellerInventory(
                seller_id=seller_id,
                product_id=data.product_id,
                quantity=data.quantity,
                price=data.price,
            )
            self.repo.create(entity)
        return JSONResponse(status_code=201, content={"detail": "Inventory created"})

    @transactional
    def update_inventory(self, data: SellerInventoryUpdate):
        entity = self.repo.get_by_id(data.id)
        if entity is None:
            raise BusinessError("Record Not Found")
        if data.quantity < 0:
            raise BusinessError("Quantity cannot be negative")
        entity.quantity = data.quantity
        entity.price = data.price
        self.repo.update(entity)
        return JSONResponse(status_code=200, content={"detail": "Inventory updated"})

    @transactional
    def delete_inventory(self, inventory_id: str):
        entity = self.repo.get_by_id(inventory_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        self.repo.delete(entity)
        return JSONResponse(status_code=200, content={"detail": "Inventory deleted"})
