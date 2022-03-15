from fastapi import Header
from presentation.http.response.task_response import TaskResponse


async def fetch_task(userId: str = Header(None)) -> list[TaskResponse]:
    pass
