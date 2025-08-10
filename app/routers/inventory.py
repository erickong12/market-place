from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.inventory import SellerInventoryCreate, SellerInventoryResponse
from app.services.inventory import SellerInventoryService

router = APIRouter(prefix="/secured/inventory", tags=["Seller Inventory"])


@router.get("/", response_model=List[SellerInventoryResponse])
def list_inventory(db: Session = Depends(get_db)):
    service = SellerInventoryService(db)
    return service.list_all_inventory()


@router.post("/", response_model=SellerInventoryResponse)
def add_inventory(
    payload: SellerInventoryCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    service = SellerInventoryService(db)
    return service.add_inventory_with_seller(payload, request.state.user.id)
