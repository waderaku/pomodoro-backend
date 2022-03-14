import uvicorn
from fastapi import FastAPI

from urls import api_routing

app = FastAPI(title="Pomodoro-Timerバックエンド")

api_routing(app)

if __name__ == "__main__":
    uvicorn.run(app, port=9000)
