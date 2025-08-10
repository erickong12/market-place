from fastapi import APIRouter, Depends, Request
from requests import Session
from app.database.session import get_db
from app.schemas.inventory import SellerInventoryCreate, SellerInventoryResponse
from app.models.inventory import SellerInventory
from typing import List

router = APIRouter(prefix="/inventory", tags=["Seller Inventory"])


@router.post("/", response_model=SellerInventoryResponse)
def add_inventory(
    payload: SellerInventoryCreate, request: Request, db: Session = Depends(get_db)
):
    inventory = SellerInventory(seller_id=request.state.user.id, **payload)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


@router.get("/", response_model=List[SellerInventoryResponse])
def list_inventory(db: Session = Depends(get_db)):
    return db.query(SellerInventory).all()
