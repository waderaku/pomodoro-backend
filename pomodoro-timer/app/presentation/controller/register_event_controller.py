import re
import traceback

from app.domain.exception.custom_exception import (
    AdditionalNegativeValueException,
    NoExistTaskException,
)
from app.presentation.http.request.register_event_request import RegisterEvent
from app.usecase.service.register_event_service import register_event_service
from fastapi import Header, HTTPException


async def register_event(request: RegisterEvent, userId: str = Header(None)):
    try:
        register_event_service(
            userId, task_id=request.taskId, start=request.start, end=request.end
        )
    except NoExistTaskException as e:
        raise HTTPException(
            status_code=404, detail=traceback.format_exception_only(type(e), e)
        )
    except AdditionalNegativeValueException as e:
        raise HTTPException(
            status_code=400, detail=traceback.format_exception_only(type(e), e)
        )
