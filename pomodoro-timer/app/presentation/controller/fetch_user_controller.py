from app.presentation.http.common.user_model import UserModel
from fastapi import Header


async def fetch_user(userId: str = Header(None)) -> UserModel:
    pass
