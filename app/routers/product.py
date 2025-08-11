from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from websockets import route

from app.database.session import get_db
from app.services.product_service import ProductService

router = APIRouter(prefix="/secured/products", tags=["Products"])


@router.get("/")
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


@router.get("/products/{product_id}")
def list_inventory(product_id: str, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.list_all_inventory(product_id)

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