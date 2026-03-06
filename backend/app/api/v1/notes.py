from fastapi import APIRouter

router = APIRouter(prefix="/v1/notes", tags=["notes"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
