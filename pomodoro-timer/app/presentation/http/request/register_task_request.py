from datetime import date

from pydantic import BaseModel


class RegisterTaskRequest(BaseModel):
    parentId: str
    name: str
    estimatedMinutes: str
    deadline: date
    notes: str
