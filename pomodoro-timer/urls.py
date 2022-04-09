from fastapi import FastAPI

from app.presentation.controller import (fetch_root_task, fetch_task,
                                         fetch_user, finish_task,
                                         register_event, register_task,
                                         update_task, update_user)
from app.presentation.http.common import UserModel
from app.presentation.http.response import RootTaskResponse, TaskResponse


def api_routing(app: FastAPI):
    app.add_api_route(
        "/rootTask",
        fetch_root_task,
        methods=["GET"],
        response_model=RootTaskResponse,
        tags=["task"],
    )
    app.add_api_route(
        "/task",
        fetch_task,
        methods=["GET"],
        response_model=list[TaskResponse],
        tags=["task"],
    )
    app.add_api_route(
        "/user",
        fetch_user,
        methods=["GET"],
        response_model=UserModel,
        tags=["user"],
    )
    app.add_api_route(
        "/task",
        register_task,
        methods=["POST"],
        tags=["task"],
    )
    app.add_api_route(
        "/task/{id}",
        update_task,
        methods=["PUT"],
        tags=["task"],
    )
    app.add_api_route(
        "/task/finish/{id}",
        finish_task,
        methods=["PUT"],
        tags=["task"],
    )
    app.add_api_route(
        "/user",
        update_user,
        methods=["PUT"],
        tags=["user"],
    )
    app.add_api_route(
        "/event",
        register_event,
        methods=["POST"],
        tags=["event"],
    )
