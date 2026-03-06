from fastapi import APIRouter

router = APIRouter(prefix="/v1/finance", tags=["finance"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
