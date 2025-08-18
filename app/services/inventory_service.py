from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.exception import BusinessError
from app.models.inventory import SellerInventory
from app.repository.inventory_repository import SellerInventoryRepository
from app.schemas.inventory import (
    SellerInventoryCreate,
    SellerInventoryPageResponse,
    SellerInventoryResponse,
    SellerInventoryUpdate,
)


class SellerInventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SellerInventoryRepository(db)

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

    def get_inventory(self, inventory_id: str) -> SellerInventoryResponse:
        entity = self.repo.get_by_id(inventory_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        return SellerInventoryResponse(**entity.__dict__)

    def add_inventory(
        self, data: SellerInventoryCreate, seller_id: str
    ) -> SellerInventoryResponse:
        entity = SellerInventory(
            seller_id=seller_id,
            product_id=data.product_id,
            quantity=data.quantity,
            price=data.price,
        )
        entity = self.repo.create(entity)
        return SellerInventoryResponse(**entity.__dict__)

    def update_inventory(self, data: SellerInventoryUpdate) -> SellerInventoryResponse:
        entity = self.repo.get_by_id(data.id)
        if entity is None:
            raise BusinessError("Record Not Found")
        if data.quantity < 0:
            raise BusinessError("Quantity cannot be negative")
        updated_entity = self.repo.update(entity, data)
        return SellerInventoryResponse(**updated_entity.__dict__)

    def delete_inventory(self, inventory_id: str):
        entity = self.repo.get_by_id(inventory_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        self.repo.delete(entity)
        return JSONResponse(status_code=204)
