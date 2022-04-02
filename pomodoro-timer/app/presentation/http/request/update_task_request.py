from datetime import date

from pydantic import BaseModel


class UpdateTaskRequest(BaseModel):
    name: str
    deadline: date
    notes: str
