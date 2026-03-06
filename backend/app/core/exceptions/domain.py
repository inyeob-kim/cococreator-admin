from app.core.exceptions.base import AppException


class NotFoundException(AppException):
    def __init__(self, *, message: str = "Resource not found", details: dict | None = None) -> None:
        super().__init__(code="NOT_FOUND", message=message, status_code=404, details=details)


class ConflictException(AppException):
    def __init__(self, *, code: str = "CONFLICT", message: str = "Conflict", details: dict | None = None) -> None:
        super().__init__(code=code, message=message, status_code=409, details=details)


class ValidationException(AppException):
    def __init__(
        self,
        *,
        code: str = "VALIDATION_ERROR",
        message: str = "Validation failed",
        details: dict | None = None,
    ) -> None:
        super().__init__(code=code, message=message, status_code=400, details=details)

