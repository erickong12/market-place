from fastapi import Request

from app.core.exception import UNAUTHORIZED


def require_roles(*roles: str):
    def checker(request: Request):
        # Middleware should set request.state.user, not just role
        user = request.state.user
        
        if roles and user.role not in roles:
            raise UNAUTHORIZED

        return user  # So endpoint can still use it
    return checker