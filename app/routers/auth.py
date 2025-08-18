from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from requests import Session

from app.database.session import get_db
from app.schemas.user import UserCreate, UserLoginResponse, UserResponse, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=UserLoginResponse)
def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.authenticate_user(credentials.username, credentials.password)


@router.post("/register")
def register_seller(data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register_user(data)


@router.get("/secured/profile", response_model=UserResponse)
def get_profile(request: Request, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.get_profile(request.state.user.id)


@router.patch("/secured/profile", response_model=UserResponse)
def update_profile(data: UserUpdate, request: Request, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.update_profile(request.state.user.id, data)


@router.patch("/secured/change-password")
def change_password(
    old_password: str,
    new_password: str,
    request: Request,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.change_password(request.state.user.id, old_password, new_password)
