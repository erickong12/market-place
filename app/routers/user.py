from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependency import require_roles
from app.services.user import UserService
from app.utils.enums import RoleEnum

router = APIRouter(
    prefix="/secured/users",
    tags=["Users"],
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)


@router.get("/")
async def list_users(
    page: int = 1,
    size: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    search: str | None = None,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service.get_user_paginated(page, size, sort_by, order, search)


@router.get("/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)
