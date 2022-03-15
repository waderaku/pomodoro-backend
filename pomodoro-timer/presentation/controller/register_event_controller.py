from fastapi import Header
from presentation.http.request.register_event_request import RegisterEvent


async def register_event(request: RegisterEvent, userId: str = Header(None)):
    pass
