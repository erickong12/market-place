from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core import config
from app.utils.enums import OrderStatus

import os
import uuid
from fastapi import UploadFile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "products")
URL_PREFIX = "/static/products"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=float(config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.ALGORITHM)
        return payload
    except JWTError:
        return None


def valid_status_transition(current: str, new: str) -> bool:
    transitions = {
        OrderStatus.PENDING.value: [
            OrderStatus.CONFIRMED.value,
            OrderStatus.CANCELLED.value,
            OrderStatus.AUTO_CANCELLED.value,
        ],
        OrderStatus.CONFIRMED.value: [
            OrderStatus.READY.value,
            OrderStatus.CANCELLED.value,
            OrderStatus.AUTO_CANCELLED.value,
        ],
        OrderStatus.READY.value: [OrderStatus.DONE.value],
        OrderStatus.DONE.value: [],
        OrderStatus.CANCELLED.value: [],
        OrderStatus.AUTO_CANCELLED.value: [],
    }
    return new in transitions.get(current, [])


async def save_upload_file(image: UploadFile | None) -> str | None:
    if not image:
        return None
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(image.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())

    return f"{URL_PREFIX}/{filename}"


def delete_file(url_path: str | None) -> None:
    if not url_path:
        return

    if url_path.startswith(URL_PREFIX):
        local_path = url_path.replace(URL_PREFIX, UPLOAD_DIR)
        if os.path.exists(local_path):
            os.remove(local_path)


def get_user_from_token(auth_header: str) -> str | None:
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        return None
    user_id: str = payload.get("data", {}).get("user_id")
    return user_id
