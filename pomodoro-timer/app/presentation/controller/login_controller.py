import traceback

from app.domain.exception.custom_exception import (
    MissMatchPasswordException,
    NoExistUserException,
    PasswordIsInvalidException,
)
from app.presentation.http.request.auth_user_request import AuthUser
from app.usecase.service.login_service import login_service
from fastapi import HTTPException


async def login(request: AuthUser):
    try:
        token_user = login_service(user_id=request.userId, password=request.password)
        return token_user._auth_token.value
    except (
        NoExistUserException,
        PasswordIsInvalidException,
        MissMatchPasswordException,
    ):
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="ユーザIDもしくはパスワードが違います")
