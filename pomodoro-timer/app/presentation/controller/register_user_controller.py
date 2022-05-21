import traceback

from app.domain.exception.custom_exception import AlreadyExistUserException
from app.usecase.service.register_user_service import register_user_service
from fastapi import Header, HTTPException


async def register_user(userId: str = Header(None)):
    try:
        register_user_service(user_id=userId)
    except AlreadyExistUserException as e:
        raise HTTPException(
            status_code=400, detail=traceback.format_exception_only(type(e), e)
        )
