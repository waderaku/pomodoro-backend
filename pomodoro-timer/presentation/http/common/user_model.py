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
    rest: int


class UserModel(BaseModel):
    isGoogleLinked: bool
    googleConfig: GoogleConfig
    defaultLength: DefaultLength
