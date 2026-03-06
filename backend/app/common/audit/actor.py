from pydantic import BaseModel


class AuditActor(BaseModel):
    user_id: int
    role: str

