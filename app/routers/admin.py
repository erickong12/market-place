from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependency import require_roles
from app.schemas.product import ProductCreate, ProductPageResponse, ProductResponse, ProductUpdate
from app.schemas.user import UserCreate, UserPageResponse
from app.services.product_service import ProductService
from app.services.user_service import UserService
from app.utils.enums import RoleEnum

router = APIRouter(
    prefix="/secured/admin",
    tags=["Admin"],
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)


@router.get("/", response_model=UserPageResponse)
async def list_users(
    page: int = 1,
    size: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service.get_paginated(page, size, sort_by, order, search)


@router.post("/")
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.insert_user(data)


@router.delete("/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_user(user_id)


@router.get("/products", response_model=ProductPageResponse)
def list_products(
    page: int = 1,
    size: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    return service.get_paginated(page, size, sort_by, order, search)


@router.post("/products")
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


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    data = ProductUpdate(id=product_id, name=name, description=description, price=price)
    return await service.update_product(data, image)


@router.delete("/products/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.delete_product(product_id)
