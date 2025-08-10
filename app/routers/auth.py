from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from requests import Session

from app.database.session import get_db
from app.schemas.user import UserCreate
from app.services import auth, user
from app.utils.enums import RoleEnum

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
    db: Session = Depends(get_db),
):
    return auth.authenticate_user(db, credentials.username, credentials.password)


@router.post("/register/seller")
def register_seller(data: UserCreate, db: Session = Depends(get_db)):
    data.role = RoleEnum.SELLER
    return user.insert_user(db, data)


@router.post("/register/buyer")
def register_seller(data: UserCreate, db: Session = Depends(get_db)):
    data.role = RoleEnum.BUYER
    return user.insert_user(db, data)
