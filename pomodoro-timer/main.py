import inject
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.domain.repository.user_repository import UserRepository
from app.infrastructure.dynamodb.repository.user_dynamo_repository import (
    UserDynamoRepository,
)
from urls import api_routing

app = FastAPI(title="Pomodoro-Timerバックエンド")

api_routing(app)


def inject_config(binder: inject.Binder):
    binder.bind(UserRepository, UserDynamoRepository())


if __name__ == "__main__":
    load_dotenv("/root/workspaces/pomodoro-backend/pomodoro-timer/app/.env")
    inject.configure(inject_config)
    uvicorn.run(app, port=9000)
