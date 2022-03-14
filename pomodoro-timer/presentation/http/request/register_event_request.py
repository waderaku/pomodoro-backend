from datetime import datetime

from pydantic import BaseModel


class RegisterEvent(BaseModel):
    taskId: str
    start: datetime
    end: datetime
