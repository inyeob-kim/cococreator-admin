from typing import Any


def success_response(data: Any, message: str = "OK") -> dict[str, Any]:
    return {"success": True, "message": message, "data": data, "error": None}


def error_response(
    *,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "success": False,
        "message": message,
        "data": None,
        "error": {"code": code, "details": details or {}},
    }

