from typing import Optional

from app.domain.model.entity.user import User
from app.domain.model.value import google_config
from app.presentation.http.common.user_model import (
    Calender,
    DefaultLength,
    GoogleConfig,
    TaskList,
    UserModel,
)
from app.usecase.service.fetch_user_service import fetch_user_service
from fastapi import Header


async def fetch_user(userId: str = Header(None)) -> UserModel:
    user = fetch_user_service(user_id=userId)
    return UserModel(
        isGoogleLinked=user._is_google_linked,
        googleConfig=create_google_config(user._google_config),
        defaultLength=DefaultLength(
            work=user._default_length.work, rest=user._default_length.rest
        ),
    )


def create_google_config(
    google_config: google_config.GoogleConfig,
) -> Optional[GoogleConfig]:
    if not google_config:
        return
    return GoogleConfig(
        calendar=Calender(
            id=google_config.calendar.id, name=google_config.calendar.name
        ),
        taskList=TaskList(
            id=google_config.task_list.id, name=google_config.task_list.name
        ),
    )
