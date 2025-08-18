from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.responses import JSONResponse


# definitions


class BusinessError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


INVALID_CREDENTIALS = HTTPException(
    detail="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED
)
UNAUTHORIZED = HTTPException(
    detail="Unauthorized", status_code=status.HTTP_403_FORBIDDEN
)


# handlers


async def http_exception_handler(request: Request, exc: Exception):
    headers = {"Access-Control-Allow-Origin": "*"}
    if isinstance(exc, HTTPException):
        return JSONResponse(
            {"detail": str(exc)}, status_code=exc.status_code, headers=headers
        )
    elif isinstance(exc, RequestValidationError):
        return JSONResponse(
            content={"message": "Invalid Request", "errors": exc.errors()},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers=headers,
        )
    elif isinstance(exc, ValidationException):
        return JSONResponse(
            content={"message": "Validation Error", "errors": exc.errors()},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers=headers,
        )
    return JSONResponse(
        content={"message": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers=headers,
    )
