from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.responses import JSONResponse


# definitions

INVALID_CREDENTIALS = HTTPException(
    detail="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED
)
UNAUTHORIZED = HTTPException(
    detail="Unauthorized", status_code=status.HTTP_403_FORBIDDEN
)
RECORD_NOT_FOUND = HTTPException(
    detail="Record not found", status_code=status.HTTP_404_NOT_FOUND
)
RECORD_ALREADY_EXISTS = HTTPException(
    detail="Record already exists", status_code=status.HTTP_409_CONFLICT
)
# handlers


async def http_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            content={"message": exc.detail}, status_code=exc.status_code
        )
    elif isinstance(exc, RequestValidationError):
        return JSONResponse(
            content={"message": "Invalid Request", "errors": exc.errors()},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    elif isinstance(exc, ValidationException):
        return JSONResponse(
            content={"message": "Validation Error", "errors": exc.errors()},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return JSONResponse(
        content={"message": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
