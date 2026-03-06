from fastapi import APIRouter

router = APIRouter(prefix="/v1/products", tags=["products"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
