from fastapi import Header
from presentation.http.response.root_task_response import RootTaskResponse


async def fetch_root_task(userId: str = Header(None)) -> RootTaskResponse:
    pass
