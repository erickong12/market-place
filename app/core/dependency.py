from functools import wraps
from fastapi import Request
from requests import Session

from app.core.exception import FORBIDDEN
from app.models.user import User


def require_roles(*roles: str):
    def checker(request: Request)-> User:
        user = request.state.user

        if roles and user.role not in roles:
            raise FORBIDDEN

        return user

    return checker

def transactional(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        db: Session = self.db
        try:
            with db.begin():
                return fn(self, *args, **kwargs)
        except Exception:
            db.rollback()
            raise
    return wrapper