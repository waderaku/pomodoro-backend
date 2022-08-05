import inject
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.domain.repository.auth_user_repository import AuthUserRepository
from app.domain.repository.task_user_repository import TaskUserRepository
from app.domain.repository.token_user_repository import TokenUserRepository
from app.domain.repository.user_repository import UserRepository
from app.infrastructure.dynamodb.repository.auth_user_dynamo_repository import (
    AuthUserDynamoRepository,
)
from app.infrastructure.dynamodb.repository.task_user_dynamo_repository import (
    TaskUserDynamoRepository,
)
from app.infrastructure.dynamodb.repository.token_user_dynamo_repository import (
    TokenUserDynamoRepository,
)
from app.infrastructure.dynamodb.repository.user_dynamo_repository import (
    UserDynamoRepository,
)
from urls import api_routing

app = FastAPI(title="Pomodoro-Timerバックエンド")

api_routing(app)
origins = [
    "http://localhost.tiangolo.com/",
    "https://localhost.tiangolo.com/",
    "http://localhost/",
    "http://localhost:3000/",
    "http://localhost:3001/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def inject_config(binder: inject.Binder):
    binder.bind(UserRepository, UserDynamoRepository())
    binder.bind(TaskUserRepository, TaskUserDynamoRepository())
    binder.bind(AuthUserRepository, AuthUserDynamoRepository())
    binder.bind(TokenUserRepository, TokenUserDynamoRepository())


if __name__ == "__main__":
    load_dotenv("/root/workspaces/pomodoro-backend/pomodoro-timer/app/.env")
    inject.configure(inject_config)
    uvicorn.run(app, port=9000)
