from sqlalchemy.orm import Session
from app.core.exception import BusinessError
from app.repository.user import UserRepository
from app.schemas.common import PageResponse
from app.schemas.user import UserPageResponse, UserResponse, UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get_user_paginated(
        self, page: int, size: int, sort_by: str, order: str, search: str | None = None
    ) -> UserPageResponse:
        skip = (page - 1) * size
        limit = size
        result = self.repo.find_all_paginated_users(skip, limit, sort_by, order, search)
        return UserPageResponse(
            page=PageResponse(
                page=page, size=size, offset=skip, total_record=result.total
            ),
            result=result.data,
        )

    def get_user_by_id(self, user_id: str) -> UserResponse:
        entity = self.repo.find_user_by_id(user_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        return UserResponse(**entity.__dict__)

    def insert_user(self, data: UserCreate) -> UserResponse:
        entity = self.repo.find_user_by_username(data.username)
        if entity is not None:
            raise BusinessError("User already exists")
        created = self.repo.create_user(data)
        return UserResponse(**created.__dict__)

    def update_user(self, data: UserUpdate) -> UserResponse:
        entity = self.repo.find_user_by_id(data.id)
        if entity is None:
            raise BusinessError("Record Not Found")
        updated = self.repo.update_user(entity, data)
        return UserResponse(**updated.__dict__)

    def delete_user(self, user_id: str) -> dict:
        entity = self.repo.find_user_by_id(user_id)
        if entity is None:
            raise BusinessError("Record Not Found")
        self.repo.delete_user(entity)
        return {"message": "User deleted successfully"}
