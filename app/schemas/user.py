from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.user import RoleEnum


class UserCreate(BaseModel):
    name: str
    address: Optional[str]
    phone: str
    username: str
    password: str
    role: RoleEnum


class UserUpdateProfile(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    username: Optional[str]


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


class UserOut(BaseModel):
    id: str
    name: str
    model_config = ConfigDict(from_attributes=True)


class UserPageResponse(BaseModel):
    page: int
    size: int
    offset: int
    total_record: int
    result: list[UserResponse]


class UserLoginResponse(BaseModel):
    access_token: str
