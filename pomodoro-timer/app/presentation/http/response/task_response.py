from datetime import date

from pydantic import BaseModel


class TaskData(BaseModel):
    name: str
    childrenIdList: list[str]
    done: bool
    finishedWorkload: int
    estimatedWorkload: int
    deadline: date
    notes: str


class Task(BaseModel):
    id: str
    taskData: TaskData


class TaskResponse(BaseModel):
    task: Task
    rootTaskId: list[str]
