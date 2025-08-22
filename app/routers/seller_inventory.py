from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.dependency import require_roles
from app.database.session import get_db
from app.schemas.inventory import (
    SellerInventoryCreate,
    SellerInventoryPageResponse,
    SellerInventoryResponse,
)
from app.schemas.product import ProductDropListResponse
from app.services.inventory_service import SellerInventoryService
from app.utils.enums import RoleEnum

router = APIRouter(
    prefix="/secured/seller-inventory",
    tags=["Seller Inventory"],
    dependencies=[Depends(require_roles(RoleEnum.SELLER))],
)


@router.get("/", response_model=SellerInventoryPageResponse)
def list_inventory(
    request: Request,
    page: int = 1,
    size: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    db: Session = Depends(get_db),
):
    service = SellerInventoryService(db)
    return service.list_all_inventory(
        page, size, sort_by, order, search, request.state.user.id
    )


@router.get("/products", response_model=list[ProductDropListResponse])
def get_product_list(db: Session = Depends(get_db)):
    service = SellerInventoryService(db)
    return service.get_product_list()


@router.post("/", response_model=SellerInventoryResponse)
def add_inventory(
    payload: SellerInventoryCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    service = SellerInventoryService(db)
    return service.add_inventory(payload, request.state.user.id)


@router.put("/{inventory_id}")
def update_inventory(
    inventory_id: str,
    payload: SellerInventoryCreate,
    db: Session = Depends(get_db),
):
    service = SellerInventoryService(db)
    return service.update_inventory(inventory_id, payload)


@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_id: str,
    db: Session = Depends(get_db),
):
    service = SellerInventoryService(db)
    return service.delete_inventory(inventory_id)
