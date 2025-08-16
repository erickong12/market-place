# app/routers/checkout.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.dependency import require_roles
from app.database.session import get_db
from app.schemas.cart import CartItemCreate
from app.services.cart_service import CartService
from app.utils.enums import RoleEnum

router = APIRouter(
    prefix="/secured/cart",
    tags=["Cart"],
    dependencies=[Depends(require_roles(RoleEnum.BUYER))],
)


@router.get("/")
def list_cart(request: Request, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.list_cart(request.state.user.id)


@router.post("/")
def checkout(items: CartItemCreate, request: Request, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.add_to_cart(request.state.user.id, items)


@router.put("/{cart_item_id}")
def update_cart_item(
    cart_item_id: str,
    quantity: int,
    request: Request,
    db: Session = Depends(get_db),
):
    service = CartService(db)
    return service.update_cart_item(cart_item_id, quantity, request.state.user.id)


@router.delete("/")
def clear_cart(request: Request, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.clear_cart(request.state.user.id)


@router.delete("/{cart_item_id}")
def delete_cart_item(
    cart_item_id: str, request: Request, db: Session = Depends(get_db)
):
    service = CartService(db)
    return service.delete_cart_item(cart_item_id, request.state.user.id)


@router.post("/checkout")
def checkout(
    request: Request,
    db: Session = Depends(get_db),
):
    service = CartService(db)
    return service.checkout(request.state.user.id)
