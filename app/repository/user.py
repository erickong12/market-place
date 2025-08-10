from requests import Session

from app.models.user import User
from app.repository.common import find_all_paginated
from app.schemas.user import UserCreate, UserUpdate
from app.utils import util


def find_all_paginated_users(
    db: Session, skip: int, limit: int, sort_by: str, order: str, search: str | None
):
    query = db.query(User)
    if search is not None:
        query = query.filter((User.name.ilike(search)) | (User.username.ilike(search)))
    return find_all_paginated(query, User, skip, limit, sort_by, order)


def find_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id, User.delete == False).first()


def find_user_by_username(db: Session, username: str):
    return (
        db.query(User).filter(User.username == username, User.delete == False).first()
    )


def create_user(db: Session, user_data: UserCreate):
    user = User(
        name=user_data.name,
        address=user_data.address,
        phone=user_data.phone,
        username=user_data.username,
        password=util.hash_password(user_data.password),
        role=user_data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, user_data: UserUpdate):
    user.name = user_data.name
    user.address = user_data.address
    user.phone = user_data.phone
    user.username = user_data.username
    if user_data.password is not None:
        user.password = util.hash_password(user_data.password)
    user.role = user_data.role
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    user.delete = True
    db.commit()
