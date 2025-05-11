from .handlers import (
    not_found_handler,
    forbidden_handler,
    invalid_error_handler,
    custom_error_handler,
)
from .custom import (
    NotFoundException,
    ForbiddenException,
    InvalidException,
    CustomErrorException,
)

exception_handlers = {
    NotFoundException: not_found_handler,
    ForbiddenException: forbidden_handler,
    InvalidException: invalid_error_handler,
    CustomErrorException: custom_error_handler,
}

__all__ = [
    "NotFoundException",
    "ForbiddenException",
    "InvalidException",
    "CustomErrorException",
    "exception_handlers",
]
