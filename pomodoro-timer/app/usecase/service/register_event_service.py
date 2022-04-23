import os
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

import boto3
from app.usecase.exception.custom_exception import (
    AdditionalNegativeValueException, NoExistTaskException)
from boto3.dynamodb.conditions import Key

table_name = "pomodoro_info"


def register_event_service(
    user_id: str,
    task_id: str,
    start: datetime,
    end: datetime,
):
    """対応するタスクのイベント情報の登録及び各タスクの作業完了時間の更新を行う

    Args:
        user_id (str): ユーザID
        task_id (str): タスクID
        start (datetime): 作業開始時間
        end (datetime): 作業終了時間
    """
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)
    # タスク一覧の取得
    task_list: list[dict] = table.query(
        KeyConditionExpression=Key("ID").eq(f"{user_id}_task")
    )["Items"]

    # 対象のタスクを取得

    response = table.get_item(Key={"ID": f"{user_id}_task", "DataType": task_id})
    task = response.get("Item", None)
    if not task:
        raise NoExistTaskException()

    parent_task_dict = _create_root_tree(task_list)
    event = {
        "ID": f"{user_id}_event",
        "DataType": start.isoformat(),
        "DataValue": task_id,
        "EndTime": end.isoformat(),
    }
    update_task_list = _add_workload(parent_task_dict, task, start, end)
    with table.batch_writer() as batch:
        for task in update_task_list:
            batch.put_item(Item=task)
        batch.put_item(Item=event)


def _add_workload(
    parent_task_dict: dict, target_task: dict, start: datetime, end: datetime
) -> list[dict]:
    additional_time = end - start
    if additional_time.total_seconds() < 0:
        raise AdditionalNegativeValueException()
    additional_workload = additional_time.total_seconds() / 60
    task_id = target_task["DataType"]
    target_task["TaskInfo"]["finished_workload"] = (
        target_task["TaskInfo"]["finished_workload"] + Decimal(additional_workload)
    ).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    update_task_list = [target_task]
    while True:
        target_task = parent_task_dict.get(task_id, None)
        if not target_task:
            break
        target_task["TaskInfo"]["finished_workload"] = (
            target_task["TaskInfo"]["finished_workload"] + Decimal(additional_workload)
        ).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

        update_task_list.append(target_task)
        task_id = target_task["DataType"]
    return update_task_list


def _create_root_tree(task_list: list[dict]) -> dict:
    root_dict = {}

    for task in task_list:
        children_id_list = task["TaskInfo"]["children_task_id"]
        for child_id in children_id_list:
            root_dict[child_id] = task

    return root_dict
