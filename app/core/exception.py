from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


# definitions


class BusinessError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


UNAUTHORIZED = HTTPException(
    detail="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED
)
FORBIDDEN = HTTPException(
    detail="Unauthorized", status_code=status.HTTP_403_FORBIDDEN
)


# handlers


async def http_exception_handler(request: Request, exc: Exception):
    headers = {"Access-Control-Allow-Origin": "*"}
    if isinstance(exc, HTTPException):
        return JSONResponse(
            {"detail": str(exc.detail)}, status_code=exc.status_code, headers=headers
        )
    elif isinstance(exc, RequestValidationError) or isinstance(exc, ValidationError):
        return JSONResponse(
            content={"detail": f"${exc.errors()}"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers=headers,
        )
    return JSONResponse(
        content={"detail": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers=headers,
    )
