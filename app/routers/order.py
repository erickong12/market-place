from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.order import OrderService
from app.core.dependency import require_roles
from app.utils.enums import RoleEnum

router = APIRouter(prefix="/secured/orders", tags=["Orders"])


@router.get("/", dependencies=[Depends(require_roles(RoleEnum.SELLER, RoleEnum.BUYER))])
def list_orders_by_seller(request: Request, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.list_orders_by_seller(request.state.user)


@router.get(
    "/{order_id}",
    dependencies=[Depends(require_roles(RoleEnum.SELLER, RoleEnum.BUYER))],
)
def get_order(order_id: str, request: Request, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.get_order(order_id, request.state.user)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch(
    "/{order_id}/confirm", dependencies=[Depends(require_roles(RoleEnum.SELLER))]
)
def confirm_order(order_id: str, request: Request, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.confirm_order(order_id, request.state.user)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch(
    "/{order_id}/reject", dependencies=[Depends(require_roles(RoleEnum.SELLER))]
)
def reject_order(order_id: str, request: Request, db: Session = Depends(get_db)):
    service = OrderService(db)
    service.reject_order(order_id, request.state.user)


@router.patch(
    "/{order_id}/ready",
    dependencies=[Depends(require_roles(RoleEnum.SELLER))],
)
def ready_order(order_id: str, request: Request, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.ready_order(order_id, request.state.user)


@router.patch("/{order_id}/done", dependencies=[Depends(require_roles(RoleEnum.BUYER))])
def complete_order(order_id: str, request: Request, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.complete_order(order_id, request.state.user)


@router.patch(
    "/{order_id}/cancel", dependencies=[Depends(require_roles(RoleEnum.BUYER))]
)
def cancel_order(order_id: str, request: Request, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.cancel_order(order_id, request.state.user)


@router.get(
    "/history", dependencies=[Depends(require_roles(RoleEnum.BUYER, RoleEnum.SELLER))]
)
def order_history(request: Request, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.get_order_history(request.state.user.id)
