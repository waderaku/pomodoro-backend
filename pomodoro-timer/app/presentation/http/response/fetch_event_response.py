from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    startTime: datetime
    endTime: datetime


class EventSummary(BaseModel):
    totalFinishedWorkload: float
    mothlyFinishedWorkload: float
    weeklyFinishedWorkload: float
    daylyFinishedWorkload: float


class EventTask(BaseModel):
    id: str
    name: str
    finishedWorkload: str
    eventList: list[Event]
