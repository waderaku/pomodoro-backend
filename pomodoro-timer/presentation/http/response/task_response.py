from datetime import date

from pydantic import BaseModel


class TaskData(BaseModel):
    name: str
    done: bool
    childrenIdList: list[str]
    finishedMinutes: int
    estimatedMinutes: int
    deadline: date
    notes: str


class TaskResponse(BaseModel):
    id: str
    task: TaskData
