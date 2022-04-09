from app.presentation.http.request.register_event_request import RegisterEvent
from fastapi import Header


async def register_event(request: RegisterEvent, userId: str = Header(None)):
    pass
