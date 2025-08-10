from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.inventory import SellerInventory
from app.schemas.inventory import SellerInventoryCreate


class SellerInventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_inventory_list(
        self, product_id: Optional[int] = None, seller_id: Optional[int] = None
    ) -> List[SellerInventory]:
        query = self.db.query(SellerInventory)
        if product_id:
            query = query.filter(SellerInventory.product_id == product_id)
        if seller_id:
            query = query.filter(SellerInventory.seller_id == seller_id)
        return query.all()

    def get_inventory_by_id(self, inventory_id: int) -> Optional[SellerInventory]:
        return (
            self.db.query(SellerInventory)
            .filter(SellerInventory.id == inventory_id)
            .first()
        )

    def get_inventory_by_product_and_seller(
        self, product_id: str, seller_id: str
    ) -> Optional[SellerInventory]:
        return (
            self.db.query(SellerInventory)
            .filter(
                SellerInventory.product_id == product_id,
                SellerInventory.seller_id == seller_id,
            )
            .first()
        )

    def create_inventory(self, data: SellerInventoryCreate) -> SellerInventory:
        db_inventory = SellerInventory(**data.model_dump())
        self.db.add(db_inventory)
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory

    def update_inventory(
        self, inventory: SellerInventory, data: SellerInventoryCreate
    ) -> SellerInventory:
        inventory.price = data.price
        inventory.quantity = data.quantity
        self.db.commit()
        self.db.refresh(inventory)
        return inventory
