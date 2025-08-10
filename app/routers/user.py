from fastapi import APIRouter, Depends
from requests import Session

from app.database.session import get_db
from app.core.dependency import require_roles
from app.services.user import get_user_by_id, get_user_paginated
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
    search: str = None,
    db: Session = Depends(get_db),
):
    return get_user_paginated(db, page, size, sort_by, order, search)


@router.get("/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)
