from app.presentation.http.common.user_model import UserModel
from fastapi import Header


async def update_user(request: UserModel, userId: str = Header(None)):
    pass
