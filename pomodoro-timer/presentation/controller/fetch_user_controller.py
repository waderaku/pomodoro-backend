from fastapi import Header
from presentation.http.common.user_model import UserModel


async def fetch_user(userId: str = Header(None)) -> list[UserModel]:
    pass
