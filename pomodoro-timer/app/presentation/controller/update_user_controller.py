from fastapi import Header
from presentation.http.common.user_model import UserModel


async def update_user(request: UserModel, userId: str = Header(None)):
    pass
