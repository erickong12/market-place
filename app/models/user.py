from uuid import uuid4

from sqlalchemy import Column, Enum, String, Boolean

from app.database.base import Base
from app.utils.enums import RoleEnum


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String)
    address = Column(String)
    username = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.BUYER)
    delete = Column(Boolean, default=False)
