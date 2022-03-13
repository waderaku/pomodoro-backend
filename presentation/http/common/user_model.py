from pydantic import BaseModel


class Calender(BaseModel):
    id: str
    name: str


class TaskList(BaseModel):
    id: str
    name: str


class GoogleConfig(BaseModel):
    calendar: Calender
    taskList: TaskList


class DefaultLength(BaseModel):
    work: int
    _break: int


class UserModel(BaseModel):
    isGoogleLinked: bool
    googleConfig: dict
    defaultLength: dict
