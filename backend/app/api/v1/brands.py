from fastapi import APIRouter

router = APIRouter(prefix="/v1/brands", tags=["brands"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
