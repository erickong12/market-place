from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.dependency import require_roles
from app.database.session import get_db
from app.schemas.inventory import SellerInventoryCreate
from app.services.inventory import SellerInventoryService
from app.utils.enums import RoleEnum

router = APIRouter(
    prefix="/secured/seller-inventory",
    tags=["Seller Inventory"],
    dependencies=[Depends(require_roles(RoleEnum.SELLER))],
)


@router.get("/")
def list_inventory(request: Request, db: Session = Depends(get_db)):
    service = SellerInventoryService(db)
    return service.list_all_inventory(request.state.user.id)


@router.post("/")
def add_inventory(
    payload: SellerInventoryCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    service = SellerInventoryService(db)
    return service.add_inventory_with_seller(payload, request.state.user.id)


@router.put("/{inventory_id}")
def update_inventory(
    inventory_id: str,
    payload: SellerInventoryCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    service = SellerInventoryService(db)
    return service.update_inventory(inventory_id, payload, request.state.user.id)


@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    service = SellerInventoryService(db)
    return service.delete_inventory(inventory_id, request.state.user.id)
