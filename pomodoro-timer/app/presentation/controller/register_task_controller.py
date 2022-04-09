from app.presentation.http.request.register_task_request import RegisterTaskRequest
from fastapi import Header


async def register_task(request: RegisterTaskRequest, userId: str = Header(None)):
    pass
