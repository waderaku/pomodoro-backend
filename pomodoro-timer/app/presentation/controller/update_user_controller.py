import traceback
from typing import Optional

from app.domain.exception.custom_exception import (NoExistUserException,
                                                   NotSettingConfigException)
from app.presentation.http.common.user_model import GoogleConfig, UserModel
from app.usecase.service.update_user_service import update_user_service
from fastapi import Header, HTTPException


async def update_user(request: UserModel, userId: str = Header(None)):

    default_length = {
        "work": request.defaultLength.work,
        "rest": request.defaultLength.rest,
    }
    try:
        update_user_service(
            user_id=userId,
            is_google_linked=request.isGoogleLinked,
            default_length=default_length,
            google_config=_create_google_config(request.googleConfig),
        )
    except NoExistUserException as e:
        raise HTTPException(
            status_code=404, detail=traceback.format_exception_only(type(e), e)
        )
    except NotSettingConfigException as e:
        raise HTTPException(
            status_code=400, detail=traceback.format_exception_only(type(e), e)
        )


def _create_google_config(google_config: Optional[GoogleConfig]):
    if not google_config:
        return
    return {
        "calendar": {
            "id": google_config.calendar.id,
            "name": google_config.calendar.name,
        },
        "task_list": {
            "id": google_config.taskList.id,
            "name": google_config.taskList.name,
        },
    }
