from requests import Session
from app.models.inventory import SellerInventory
from app.schemas.inventory import SellerInventoryCreate


def create_inventory(db: Session, data: SellerInventoryCreate):
    db_inventory = SellerInventory(**data)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory
