import traceback

from app.domain.exception.custom_exception import (
    AlreadyDoneParentTaskException,
    NoExistParentTaskException,
    NoExistUserException,
    NotShortcutTaskException
)
from app.presentation.http.request.register_task_request import RegisterTaskRequest
from app.usecase.service.register_task_service import register_task_service
from fastapi import Header, HTTPException


async def register_task(request: RegisterTaskRequest, userId: str = Header(None)):
    try:
        task = register_task_service(
            user_id=userId,
            parent_id=request.parentId,
            name=request.name,
            estimated_workload=request.estimatedWorkload,
            deadline=request.deadline,
            notes=request.notes,
            shortcutFlg=request.shortcutFlg,
        )
    except (NoExistUserException, NoExistParentTaskException) as e:
        raise HTTPException(
            status_code=404, detail=traceback.format_exception_only(type(e), e)
        )
    except (AlreadyDoneParentTaskException, NotShortcutTaskException) as e:
        raise HTTPException(
            status_code=400, detail=traceback.format_exception_only(type(e), e)
        )
