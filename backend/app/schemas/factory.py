from pydantic import BaseModel


class FactoryBase(BaseModel):
    name: str
