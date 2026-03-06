from fastapi import APIRouter

router = APIRouter(prefix="/v1/orders", tags=["orders"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
