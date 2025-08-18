from sqlalchemy.orm import Session
from app.core.exception import BusinessError
from app.repository.user_repository import UserRepository
from app.schemas.user import UserPageResponse, UserResponse, UserCreate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get_paginated(
        self, page: int, size: int, sort_by: str, order: str, search: str | None = None
    ) -> UserPageResponse:
        skip = (page - 1) * size
        limit = size
        result = self.repo.find_all_paginated(skip, limit, sort_by, order, search)
        return UserPageResponse(
            page=page,
            size=size,
            skip=skip,
            total_record=result.total,
            result=result.data,
        )

    def insert_user(self, data: UserCreate) -> UserResponse:
        entity = self.repo.find_by_username(data.username)
        if entity is not None:
            raise BusinessError("User already exists")
        created = self.repo.save(data)
        return UserResponse(**created.__dict__)

    def delete_user(self, user_id: str) -> dict:
        entity = self.repo.find_by_id(user_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        self.repo.delete(entity)
        return {"message": "User deleted successfully"}
