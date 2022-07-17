from datetime import date

from pydantic import BaseModel


class TaskData(BaseModel):
    name: str
    childrenIdList: list[str]
    parentId: str
    done: bool
    finishedWorkload: int
    estimatedWorkload: int
    deadline: date
    notes: str


class TaskModel(BaseModel):
    id: str
    taskData: TaskData


class TaskResponse(BaseModel):
    task: list[TaskModel]
    shortcutTaskId: list[str]
