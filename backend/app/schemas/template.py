from pydantic import BaseModel


class TemplateBase(BaseModel):
    name: str
