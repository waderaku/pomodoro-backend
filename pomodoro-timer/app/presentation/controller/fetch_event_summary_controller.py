from datetime import date

from app.presentation.http.response.fetch_event_response import EventSummary
from fastapi import Header


async def fetch_event_summary(
    base_date: date, userId: str = Header(None)
) -> EventSummary:
    pass
