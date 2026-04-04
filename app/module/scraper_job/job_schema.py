from pydantic import (
    BaseModel,
)
from datetime import datetime

class JobSchema(BaseModel):
    id: int
    title: str | None
    company: str | None
    location:str | None
    link: str | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True

