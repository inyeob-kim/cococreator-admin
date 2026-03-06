from fastapi import APIRouter

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
