from requests import Session
from app.core import exception
from app.models.inventory import SellerInventory
from app.schemas.inventory import SellerInventoryCreate, SellerInventoryUpdate


def get_inventory_by_id(db: Session, inventory_id: str):
    inventory = (
        db.query(SellerInventory).filter(SellerInventory.id == inventory_id).first()
    )
    if inventory is None:
        raise exception.RECORD_NOT_FOUND
    return inventory


def add_inventory(db: Session, data: SellerInventoryCreate):
    db_inventory = SellerInventory(**data)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


def update_inventory(db: Session, data: SellerInventoryUpdate):
    inventory = db.query(SellerInventory).filter(SellerInventory.id == data.id).first()
    if inventory is None:
        raise exception.RECORD_NOT_FOUND
    inventory.product = data.product
    inventory.price = data.price
    inventory.quantity = data.quantity
    db.commit()
    db.refresh(inventory)
    return inventory
