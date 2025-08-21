from sqlalchemy.orm import Session
from app.models.user import User
from app.repository.common import find_paginated
from typing import Optional


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = User

    def find_all_paginated(
        self, skip: int, limit: int, sort_by: str, order: str, search: str | None
    ):
        query = self.db.query(self.model).filter(self.model.delete == False)

        if search:
            query = query.filter(
                self.model.username.icontains(search)
                | self.model.name.icontains(search)
            )
        return find_paginated(query, self.model, skip, limit, sort_by, order)

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(self.model).filter(self.model.id == user_id).filter(self.model.delete == False).first()

    def find_by_username(self, username: str) -> Optional[User]:
        return self.db.query(self.model).filter(self.model.username == username).filter(self.model.delete == False).first()

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, entity: User) -> User:
        self.db.commit()
        return entity

    def delete(self, entity: User) -> None:
        entity.delete = True
        self.db.commit()
