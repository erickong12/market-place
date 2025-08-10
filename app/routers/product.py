from fastapi import APIRouter, Depends, File, Form, UploadFile
from requests import Session

from app.database.session import get_db
from app.core.dependency import require_roles
from app.schemas.product import ProductCreate, ProductPageResponse
from app.services import product
from app.utils.enums import RoleEnum

router = APIRouter(prefix="/secured/products", tags=["Products"])


@router.get("/", response_model=ProductPageResponse)
def list_products(
    page: int = 1,
    size: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    search: str = None,
    db: Session = Depends(get_db),
):
    return product.get_product_paginated(db, page, size, sort_by, order, search)


@router.post("/create", dependencies=[Depends(require_roles(RoleEnum.ADMIN))])
async def add_product(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    data = ProductCreate(
        name=name,
        description=description,
        price=price,
    )
    return product.insert_product(db, data, image)


@router.put("/update", dependencies=[Depends(require_roles(RoleEnum.ADMIN))])
async def update_product(
    id: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    data = ProductCreate(
        id=id,
        name=name,
        description=description,
        price=price,
    )
    return product.update_product(db, data, image)