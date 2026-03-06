from datetime import datetime

from pydantic import BaseModel


class AuditEvent(BaseModel):
    event_type: str
    entity_type: str
    entity_id: int
    actor_user_id: int
    occurred_at: datetime
    metadata: dict | None = None

