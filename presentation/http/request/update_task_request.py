from datetime import date

from pydantic import BaseModel


class UpdateTaskRequest(BaseModel):
    name: str
    deadLine: date
    notes: str
