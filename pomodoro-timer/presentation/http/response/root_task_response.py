from pydantic import BaseModel


class RootTaskResponse(BaseModel):
    taskList: list[str]
    rootList: list[str]
