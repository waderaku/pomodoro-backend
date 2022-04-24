from app.usecase.service.register_user_service import register_user_service
from fastapi import Header


async def register_user(userId: str = Header(None)):
    register_user_service(userId)
