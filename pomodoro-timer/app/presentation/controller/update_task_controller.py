import traceback

from app.domain.exception.custom_exception import NoExistTaskException
from app.presentation.http.request.update_task_request import UpdateTaskRequest
from app.usecase.service.update_task_service import update_task_service
from fastapi import Header, HTTPException


async def update_task(id: str, request: UpdateTaskRequest, userId: str = Header(None)):
    try:
        update_task_service(
            userId,
            id,
            request.name,
            request.estimatedWorkload,
            request.deadline,
            request.notes,
            request.done,
        )
    except NoExistTaskException as e:
        raise HTTPException(
            status_code=404, detail=traceback.format_exception_only(type(e), e)
        )
