from pydantic import BaseModel


class RootTaskResponse(BaseModel):
    taskList: list[str]
    root_list: list[str]
