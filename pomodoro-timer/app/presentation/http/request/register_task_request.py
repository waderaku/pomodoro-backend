from datetime import date

from pydantic import BaseModel


class RegisterTaskRequest(BaseModel):
    parentId: str
    name: str
    estimatedWorkload: str
    deadline: date
    notes: str
