from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.common.api.response import error_response
from app.core.exceptions.base import AppException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
        payload = error_response(code=exc.code, message=exc.message, details=exc.details)
        return JSONResponse(status_code=exc.status_code, content=payload)

