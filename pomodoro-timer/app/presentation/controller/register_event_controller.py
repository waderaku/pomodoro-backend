import re

from app.presentation.http.request.register_event_request import RegisterEvent
from app.usecase.service.register_event_service import register_event_service
from fastapi import Header


async def register_event(request: RegisterEvent, userId: str = Header(None)):
    register_event_service(
        userId, task_id=request.taskId, start=request.start, end=request.end
    )
