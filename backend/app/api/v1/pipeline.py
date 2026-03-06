from fastapi import APIRouter

router = APIRouter(prefix="/v1/pipeline", tags=["pipeline"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
