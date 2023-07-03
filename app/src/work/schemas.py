
from pydantic import BaseModel


class WorkplaceCreate(BaseModel):
    name: str
    key: str
