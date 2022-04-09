from app.presentation.http.response.root_task_response import RootTaskResponse
from fastapi import Header


async def fetch_root_task(userId: str = Header(None)) -> RootTaskResponse:
    pass
