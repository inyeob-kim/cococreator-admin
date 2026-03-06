from fastapi import APIRouter

router = APIRouter(prefix="/v1/factories", tags=["factories"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
