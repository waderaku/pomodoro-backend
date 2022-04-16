from datetime import date

from pydantic import BaseModel


class UpdateTaskRequest(BaseModel):
    name: str
    deadline: date
    estimatedWorkload: int
    notes: str
    done: bool
