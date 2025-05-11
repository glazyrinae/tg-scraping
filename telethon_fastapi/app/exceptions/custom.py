from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(
        self, detail: str = "Канал не существует или не найден", error_code: str = ""
    ):
        super().__init__(status_code=404, detail=detail)
        self.error_code = error_code


class ForbiddenException(HTTPException):
    def __init__(
        self, detail: str = "Доступ к частному каналу запрещен", error_code: str = ""
    ):
        super().__init__(status_code=403, detail=detail)
        self.error_code = error_code


class InvalidException(HTTPException):
    def __init__(
        self, detail: str = "Неверный формат для запроса", error_code: str = ""
    ):
        super().__init__(status_code=400, detail=detail)
        self.error_code = error_code


class CustomErrorException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = ""):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
