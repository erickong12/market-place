from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order import OrderService
from app.core.dependency import require_roles
from app.utils.enums import RoleEnum

router = APIRouter(prefix="/orders", tags=["Orders"])


# Buyer places a new order
@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    buyer_id = request.state.user.id
    service = OrderService(db)
    return service.create_order(buyer_id, order_data)


# Buyer views their order history
@router.get("/buyer", response_model=List[OrderResponse])
def get_buyer_orders(
    request: Request,
    db: Session = Depends(get_db),
):
    buyer_id = request.state.user.id
    service = OrderService(db)
    return service.get_orders_by_buyer(buyer_id)


# Seller views their order history
@router.get(
    "/seller",
    response_model=List[OrderResponse],
    dependencies=[Depends(require_roles(RoleEnum.SELLER))],
)
def get_seller_orders(
    request: Request,
    db: Session = Depends(get_db),
):
    seller_id = request.state.user.id
    service = OrderService(db)
    return service.get_orders_by_seller(seller_id)


# Seller updates order status (confirm, reject, ready to pickup, done, cancel)
@router.patch(
    "/{order_id}/status",
    dependencies=[Depends(require_roles(RoleEnum.SELLER))],
)
def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    seller_id = request.state.user.id
    service = OrderService(db)
    try:
        updated_order = service.update_order_status(
            order_id, status_update.status, seller_id
        )
        return updated_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
