from fastapi import APIRouter

from app.common.api.response import success_response

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return success_response({"status": "ok"})

