from app.core.exceptions.base import AppException


class UnauthorizedException(AppException):
    def __init__(
        self,
        *,
        code: str = "UNAUTHORIZED",
        message: str = "Unauthorized",
        details: dict | None = None,
    ) -> None:
        super().__init__(code=code, message=message, status_code=401, details=details)


class ForbiddenException(AppException):
    def __init__(
        self,
        *,
        code: str = "FORBIDDEN",
        message: str = "Forbidden",
        details: dict | None = None,
    ) -> None:
        super().__init__(code=code, message=message, status_code=403, details=details)

