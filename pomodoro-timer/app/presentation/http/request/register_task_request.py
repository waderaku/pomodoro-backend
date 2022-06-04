from datetime import date

from pydantic import BaseModel


class RegisterTaskRequest(BaseModel):
    parentId: str
    name: str
    estimatedWorkload: int
    deadline: date
    notes: str
    shortcutFlg: bool
