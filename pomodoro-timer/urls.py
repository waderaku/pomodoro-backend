from fastapi import FastAPI

from app.presentation.controller import (
    fetch_task,
    fetch_user,
    register_event,
    register_task,
    update_task,
    update_user,
)
from app.presentation.http.common import UserModel
from app.presentation.http.response import TaskResponse


def api_routing(app: FastAPI):
    app.add_api_route(
        "/task",
        fetch_task,
        methods=["GET"],
        response_model=TaskResponse,
        tags=["task"],
        description="""
        ユーザIDに紐づくタスク一覧（完了済み/未済問わず）を取得する。
        また、当該タスク一覧の中で、ルートタスクに該当するタスクIDの一覧を取得する
        """,
    )
    app.add_api_route(
        "/task",
        register_task,
        methods=["POST"],
        tags=["task"],
        description="""
        タスクを新規に登録する。
        IDはuuidによって一意に登録される。
        親タスクの作業見積時間の再計算が行われる。
        """,
    )
    app.add_api_route(
        "/task/{id}",
        update_task,
        methods=["PUT"],
        tags=["task"],
        description="""
        タスクのデータを更新する。
        親タスクの作業見積時間の再計算が行われる。
        あるタスクを完了に変更した場合、その子タスクも完了にする。
        """,
    )
    app.add_api_route(
        "/user",
        fetch_user,
        methods=["GET"],
        response_model=UserModel,
        tags=["user"],
        description="""
        ユーザ情報を取得する
        """,
    )
    app.add_api_route(
        "/user",
        update_user,
        methods=["POST"],
        tags=["user"],
        description="""
        ユーザ情報を初期登録する。
        実APIとして呼び出される想定はないが、WebSocket通信が開始した際に当該ユーザが存在しない場合に本ユースケースが走る
        """,
    )
    app.add_api_route(
        "/user",
        update_user,
        methods=["PUT"],
        tags=["user"],
        description="""
        ユーザ情報を更新する
        """,
    )
    app.add_api_route(
        "/event",
        register_event,
        methods=["POST"],
        tags=["event"],
        description="""
        作業情報を登録する。当該タスクとその親タスクの作業時間の再計算が行われる。
        """,
    )
