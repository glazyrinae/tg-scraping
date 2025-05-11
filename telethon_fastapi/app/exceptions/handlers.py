from fastapi.responses import JSONResponse
from .custom import (
    NotFoundException,
    ForbiddenException,
    InvalidException,
    CustomErrorException,
)


async def not_found_handler(request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": exc.detail, "code": exc.error_code},
    )


async def forbidden_handler(request, exc: ForbiddenException):
    return JSONResponse(
        status_code=403,
        content={"error": exc.detail, "code": exc.error_code},
    )


async def custom_error_handler(request, exc: CustomErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "code": exc.error_code},
    )


async def invalid_error_handler(request, exc: InvalidException):
    return JSONResponse(
        status_code=400,
        content={"error": exc.detail, "code": exc.error_code},
    )
