from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.order_service import OrderService
from app.core.dependency import require_roles
from app.utils.enums import OrderStatus, RoleEnum

router = APIRouter(prefix="/secured/orders", tags=["Orders"])


@router.get("/")
def list_orders(
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    order: str = "desc",
    user: Depends = require_roles(RoleEnum.SELLER, RoleEnum.BUYER),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.list_orders(page, size, sort_by, order, user)


@router.get(
    "/items/{order_id}",
    dependencies=[Depends(require_roles(RoleEnum.SELLER, RoleEnum.BUYER))],
)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.get_order_items(order_id)


@router.patch("/{order_id}/confirm")
def confirm_order(
    order_id: str,
    user: Depends = require_roles(RoleEnum.SELLER),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.update_order_status(order_id, OrderStatus.CONFIRMED, user)


@router.patch("/{order_id}/reject")
def reject_order(
    order_id: str,
    user: Depends = require_roles(RoleEnum.SELLER),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.update_order_status(order_id, OrderStatus.CANCELLED, user)


@router.patch("/{order_id}/ready")
def ready_order(
    order_id: str,
    user: Depends = require_roles(RoleEnum.SELLER),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.update_order_status(order_id, OrderStatus.READY, user)


@router.patch("/{order_id}/done")
def complete_order(
    order_id: str,
    user: Depends = require_roles(RoleEnum.SELLER),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.update_order_status(order_id, OrderStatus.DONE, user)


@router.patch("/{order_id}/cancel")
def cancel_order(
    order_id: str,
    user: Depends = require_roles(RoleEnum.SELLER),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.update_order_status(order_id, OrderStatus.CANCELLED, user)


@router.get("/history")
def order_history(
    user: Depends = require_roles(RoleEnum.SELLER, RoleEnum.BUYER),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.get_order_history(user)
