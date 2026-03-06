from fastapi import APIRouter

router = APIRouter(prefix="/v1/templates", tags=["templates"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
