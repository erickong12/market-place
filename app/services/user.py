from requests import Session
from app.core.exception import RECORD_ALREADY_EXISTS, RECORD_NOT_FOUND
from app.repository import user
from app.schemas.common import PageResponse
from app.schemas.user import UserPageResponse, UserResponse, UserCreate, UserUpdate


def get_user_paginated(
    db: Session, page: int, size: int, sort_by: str, order: str, search: str | None
):
    skip = (page - 1) * size
    limit = size
    result = user.find_all_paginated_users(db, skip, limit, sort_by, order, search)
    return UserPageResponse(
        page=PageResponse(page=page, size=size, offset=skip, total_record=result.total),
        result=result.data,
    )


def get_user_by_id(db: Session, user_id: str):
    entity = user.find_user_by_id(db, user_id)
    if user is None:
        raise RECORD_NOT_FOUND
    return UserResponse(**entity.__dict__)


def insert_user(db: Session, data: UserCreate):
    entity = user.find_user_by_username(db, data.username)
    if entity is not None:
        raise RECORD_ALREADY_EXISTS
    return UserResponse(**user.create_user(db, data).__dict__)


def update_user(db: Session, data: UserUpdate):
    entity = user.find_user_by_id(db, data.id)
    if user is None:
        raise RECORD_NOT_FOUND
    return UserResponse(**user.update_user(db, entity, data).__dict__)
