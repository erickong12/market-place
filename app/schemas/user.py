from pydantic import BaseModel, ConfigDict

from app.models.user import RoleEnum


class UserCreate(BaseModel):
    name: str
    address: str | None
    phone: str
    username: str
    password: str
    role: RoleEnum


class UserUpdateProfile(BaseModel):
    name: str
    address: str | None
    phone: str
    username: str


class UserUpdate(UserCreate):
    id: str


class UserResponse(BaseModel):
    id: str
    name: str
    username: str
    phone: str
    address: str
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)


class UserPageResponse(BaseModel):
    page: int
    size: int
    skip: int
    total_record: int
    result: list[UserResponse]


class UserLoginResponse(BaseModel):
    access_token: str


class UserToken(BaseModel):
    id: str
    role: RoleEnum


class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str
