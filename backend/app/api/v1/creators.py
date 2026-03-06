from fastapi import APIRouter

router = APIRouter(prefix="/v1/creators", tags=["creators"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
