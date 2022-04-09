from app.presentation.http.response.task_response import TaskResponse
from fastapi import Header


async def fetch_task(userId: str = Header(None)) -> list[TaskResponse]:
    pass
