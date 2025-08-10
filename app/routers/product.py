from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependency import require_roles
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductPageResponse,
    ProductResponse,
)
from app.services.product import ProductService
from app.utils.enums import RoleEnum

router = APIRouter(prefix="/secured/products", tags=["Products"])


@router.get("/", response_model=ProductPageResponse)
def list_products(
    page: int = 1,
    size: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    return service.get_product_paginated(page, size, sort_by, order, search)


@router.post(
    "/create",
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
    response_model=ProductResponse,
)
async def add_product(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    data = ProductCreate(name=name, description=description, price=price)
    return await service.insert_product(data, image)


@router.put(
    "/update",
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
    response_model=ProductResponse,
)
async def update_product(
    id: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    data = ProductUpdate(id=id, name=name, description=description, price=price)
    return await service.update_product(data, image)
