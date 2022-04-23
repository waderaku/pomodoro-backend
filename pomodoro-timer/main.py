import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from urls import api_routing

app = FastAPI(title="Pomodoro-Timerバックエンド")

api_routing(app)

if __name__ == "__main__":
    load_dotenv("/root/workspaces/pomodoro-backend/pomodoro-timer/app/.env")
    uvicorn.run(app, port=9000)
