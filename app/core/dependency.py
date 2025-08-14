from fastapi import Request

from app.core.exception import UNAUTHORIZED


def require_roles(*roles: str):
    def checker(request: Request):
        user = request.state.user

        if roles and user.role not in roles:
            raise UNAUTHORIZED

        return user

    return checker
