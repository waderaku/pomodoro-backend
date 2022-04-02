from fastapi import Header
from presentation.http.request.register_task_request import RegisterTaskRequest


async def register_task(request: RegisterTaskRequest, userId: str = Header(None)):
    pass
