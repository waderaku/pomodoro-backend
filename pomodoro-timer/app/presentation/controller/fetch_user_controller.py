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
    user = fetch_user_service(userId)
    return UserModel(
        isGoogleLinked=user.is_google_linked,
        googleConfig=create_google_config(user.google_config),
        defaultLength=DefaultLength(**user.default_length),
    )


def create_google_config(google_config: dict | None) -> GoogleConfig | None:
    if not google_config:
        return
    return GoogleConfig(
        Calender(**google_config["calender"]), TaskList(**google_config["task_list"])
    )
