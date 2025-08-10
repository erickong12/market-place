from requests import Session
from app.core.exception import INVALID_CREDENTIALS
from app.repository.user import find_user_by_username
from app.schemas.user import UserLoginResponse
from app.utils.util import create_access_token, verify_password


def authenticate_user(db: Session, username: str, password: str):
    result = find_user_by_username(db, username)
    if not result or not verify_password(password, result.password):
        raise INVALID_CREDENTIALS
    return UserLoginResponse(
        access_token=create_access_token({"data": {"user_id": result.id}}),
        token_type="bearer",
    )