from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    priority: str | None = "medium"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str | None
    due_date: datetime | None
    user_id: int

    class Config:
        from_attributes = True