from sqlalchemy.orm import Session
from app.models.user import User
from app.repository.common import find_all_paginated
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all_paginated_users(
        self, skip: int, limit: int, sort_by: str, order: str, search: Optional[str]
    ):
        query = self.db.query(User)

        if search:
            query = query.filter(
                User.username.icontains(search) | User.name.icontains(search)
            )
        return find_all_paginated(query, User, skip, limit, sort_by, order)

    def find_user_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, entity: User, data: UserUpdate) -> User:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(entity, field, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_user(self, entity: User) -> None:
        entity.delete = True
        self.db.commit()
