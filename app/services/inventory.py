from sqlalchemy.orm import Session
from app.core.exception import BusinessError
from app.repository.inventory import SellerInventoryRepository
from app.schemas.inventory import (
    SellerInventoryCreate,
    SellerInventoryResponse,
    SellerInventoryUpdate,
)


class SellerInventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SellerInventoryRepository(db)

    def list_all_inventory(self) -> list[SellerInventoryResponse]:
        entities = self.repo.get_inventory_list()
        return [SellerInventoryResponse(**e.__dict__) for e in entities]

    def get_inventory(self, inventory_id: int) -> SellerInventoryResponse:
        entity = self.repo.get_inventory_by_id(inventory_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        return SellerInventoryResponse(**entity.__dict__)

    def add_inventory_with_seller(
        self, data: SellerInventoryCreate, seller_id: int
    ) -> SellerInventoryResponse:
        data.seller_id = seller_id
        entity = self.repo.create_inventory(data)
        return SellerInventoryResponse(**entity.__dict__)

    def update_stock(self, data: SellerInventoryUpdate) -> SellerInventoryResponse:
        entity = self.repo.get_inventory_by_id(data.id)
        if entity is None:
            raise BusinessError("Record Not Found")
        updated_entity = self.repo.update_inventory(entity, data)
        return SellerInventoryResponse(**updated_entity.__dict__)
