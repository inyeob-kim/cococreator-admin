from pydantic import BaseModel


class NoteBase(BaseModel):
    entity_type: str
    entity_id: int
    content: str
