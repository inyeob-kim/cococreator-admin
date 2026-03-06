from pydantic import BaseModel


class CreatorBase(BaseModel):
    name: str
