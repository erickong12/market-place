from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core import config
from app.utils.enums import OrderStatus


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
