import traceback

from app.domain.exception.custom_exception import (DeleteRootTaskException,
                                                   NoExistTaskException,
                                                   NoExistUserException)
from app.usecase.service.delete_task_service import delete_task_service
from fastapi import Header, HTTPException


async def delete_task(id: str, userId: str = Header(None)):
    try:
        delete_task_service(user_id=userId, task_id=id)
    except (NoExistTaskException, NoExistUserException) as e:
        raise HTTPException(
            status_code=404, detail=traceback.format_exception_only(type(e), e)
        )
    except DeleteRootTaskException as e:
        raise HTTPException(
            status_code=400, detail=traceback.format_exception_only(type(e), e)
        )
