from fastapi import Request

from app.core.exception import UNAUTHORIZED
from app.models.user import User


def require_roles(*roles: str):
    def checker(request: Request)-> User:
        user = request.state.user

        if roles and user.role not in roles:
            raise UNAUTHORIZED

        return user

    return checker
