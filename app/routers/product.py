from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from websockets import route

from app.core.dependency import require_roles
from app.database.session import get_db
from app.services.inventory_service import SellerInventoryService
from app.services.product_service import ProductService
from app.utils.enums import RoleEnum

router = APIRouter(
    prefix="/secured/products",
    tags=["Products"],
    dependencies=[Depends(require_roles(RoleEnum.BUYER))],
)


@router.get("/inventory")
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
    return service.list_all_inventory(page, size, sort_by, order, search)


@route.post("/landing")
def landing_page(
    page: int = 1,
    size: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    return service.get_landing_page(page, size, sort_by, order, search)
