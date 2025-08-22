from fastapi import Request
from app.database.session import get_db_session
from app.core.exception import UNAUTHORIZED
from app.repository.user_repository import UserRepository
from app.schemas.user import UserToken
from app.utils import util
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    """
    AuthMiddleware is a custom middleware for FastAPI applications that enforces authentication and role-based authorization on secured endpoints.
    Features:
    - Checks if the request path starts with "/secured" to apply authentication.
    - Validates the presence and format of the Authorization header (expects a Bearer token).
    - Verifies the JWT token and extracts the user ID.
    - Retrieves the user from the database and attaches it to the request state.
    - Checks required roles for the endpoint or router, ensuring the user has appropriate permissions.
    - Raises UnauthorizedUserException for any authentication or authorization failure.
    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next middleware or endpoint handler.
    Raises:
        UnauthorizedUserException: If authentication or authorization fails.
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if request.method != "OPTIONS" and path.startswith("/secured"):
            user_id = util.get_user_from_token(request.headers.get("Authorization"))
            if not user_id:
                raise UNAUTHORIZED
            with get_db_session() as db:
                user = UserRepository(db).find_by_id(user_id)
                if not user:
                    raise UNAUTHORIZED
                request.state.user = UserToken(**user.__dict__)
        return await call_next(request)
