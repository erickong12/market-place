from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.exception import INVALID_CREDENTIALS
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserLoginResponse,
    UserResponse,
    UserUpdateProfile,
)
from app.utils import util
from app.utils.util import create_access_token, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def authenticate_user(self, username: str, password: str):
        result = self.repo.find_by_username(username)
        if not result or not verify_password(password, result.password):
            raise INVALID_CREDENTIALS
        return UserLoginResponse(
            access_token=create_access_token({"data": {"user_id": result.id}})
        )

    def get_profile(self, user_id: str):
        user = self.repo.find_by_id(user_id)
        if not user:
            raise INVALID_CREDENTIALS("User not found")
        return UserResponse(**user.__dict__)

    def register_user(self, data: UserCreate):
        existing_user = self.repo.find_by_username(data.username)
        if existing_user:
            raise INVALID_CREDENTIALS("User already exists")
        user = User(
            name=data.name,
            address=data.address,
            phone=data.phone,
            username=data.username,
            password=util.hash_password(data.password),
            role=data.role,
        )
        self.repo.save(user)
        return JSONResponse(status_code=201)

    def update_profile(self, user_id: str, data: UserUpdateProfile):
        user = self.repo.find_by_id(user_id)
        if not user:
            raise INVALID_CREDENTIALS("User not found")
        user.username = data.username
        user.name = data.name
        user.phone = data.phone
        user.address = data.address
        self.repo.update(user)
        return UserResponse(**user.__dict__)

    def change_password(self, user_id: str, old_password: str, new_password: str):
        user = self.repo.find_by_id(user_id)
        if not user or not verify_password(old_password, user.password):
            raise INVALID_CREDENTIALS
        user.password = util.hash_password(new_password)
        self.repo.update(user)
        return JSONResponse(status_code=200)
