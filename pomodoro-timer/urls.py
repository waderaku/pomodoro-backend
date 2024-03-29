from fastapi import FastAPI

from app.presentation.controller import (delete_task, fetch_event_summary,
                                         fetch_task, fetch_user,
                                         register_event, register_task,
                                         register_user, search_event_task,
                                         update_task, update_user)
from app.presentation.http.common import UserModel
from app.presentation.http.response import TaskResponse
from app.presentation.http.response.fetch_event_response import (EventSummary,
                                                                 EventTask)


def api_routing(app: FastAPI):
    app.add_api_route(
        "/task",
        fetch_task,
        methods=["GET"],
        response_model=TaskResponse,
        tags=["task"],
        description="""
        ユーザIDに紐づくタスク一覧（完了済み/未済問わず）を取得する。
        タスク内には、全ての親タスクとなる「root」タスクも含む。
        また、当該タスク一覧の中で、ショートカットに登録されているタスクIDの一覧を取得する
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
        ルートタスクの場合、parentIdはrootとする。
        今回の更新により、親タスクの作業見積時間を、本タスク含めた子タスクの合計作業見積もり時間が
        上回った場合、親タスクの作業見積時間を子タスクの合計作業見積時間に更新する。
        また、今回の更新により、親タスクの期日より本タスクの期日が後日の場合、親タスクの期日を子タスクの期日に更新する。
        """,
    )
    app.add_api_route(
        "/task/{id}",
        update_task,
        methods=["PUT"],
        tags=["task"],
        description="""
        タスクのデータを更新する。
        今回の更新により、親タスクの作業見積時間を、本タスク含めた子タスクの合計作業見積もり時間が
        上回った場合、親タスクの作業見積時間を子タスクの合計作業見積時間に更新する。
        また、今回の更新により、親タスクの期日より本タスクの期日が後日の場合、親タスクの期日を子タスクの期日に更新する。
        本タスクを完了に変更した場合、その子タスクも完了にする。
        """,
    )
    app.add_api_route(
        "/task/{id}",
        delete_task,
        methods=["DELETE"],
        tags=["task"],
        description="""
        タスクのデータを削除する。
        当該タスクが子タスクも所持していた場合、当該タスクの子タスクも含めてすべて削除する
        タスクのイベント情報については残る
        """,
    )
    app.add_api_route(
        "/task/{id}/event",
        search_event_task,
        response_model=EventTask,
        methods=["GET"],
        tags=["task", "event"],
        description="""
        指定した期間(YYYY-MM-dd)に行われたタスク一覧と、各タスクの期間内の作業時間を取得する
        idに指定されたタスクに紐づく子タスク単位で取得する
        ただし、対象となるタスクの子タスクのイベントも全て対象となる
        idがrootであった場合、rootTaskを取得する
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
        register_user,
        methods=["POST"],
        tags=["user"],
        description="""
        ユーザ情報を初期登録する。
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
        作業情報を登録する。当該タスクとその親タスクの作業時間に、今回の作業時間を追加するが行われる。
        """,
    )
    app.add_api_route(
        "/event/summary",
        fetch_event_summary,
        response_model=EventSummary,
        methods=["GET"],
        tags=["event"],
        description="""
        基準日（YYYY-MM-dd）から見ての当月、当週及び当日を含めた
        これまでの作業時間のサマリーを取得する
        単位はhourを小数点第一位までで返却する
        """,
    )
