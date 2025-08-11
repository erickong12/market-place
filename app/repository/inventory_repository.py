# app/repository/inventory.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.inventory import SellerInventory
from app.repository.common import find_paginated
from app.schemas.inventory import SellerInventoryCreate


class SellerInventoryRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = SellerInventory

    def get_inventory_list_by_seller(
        self,
        skip: int,
        limit: int,
        sort_by: str,
        order: str,
        seller_id: str,
        search: Optional[str],
    ) -> List[SellerInventory]:
        query = self.db.query(self.model).filter(self.model.seller_id == seller_id)
        if search is not None:
            query = query.filter(self.model.product.name.icontains(search))
        return find_paginated(query, self.model, skip, limit, sort_by, order)
    
    

    def create(self, seller_id: str, data: SellerInventoryCreate):
        inv = SellerInventory(seller_id=seller_id, **data.model_dump())
        self.db.add(inv)
        self.db.flush()
        return inv

    def get_inventory_for_update(self, inv_id: str):
        return (
            self.db.query(SellerInventory)
            .filter(SellerInventory.id == inv_id)
            .with_for_update()
            .first()
        )
