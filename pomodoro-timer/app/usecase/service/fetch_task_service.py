import os
from dataclasses import dataclass
from datetime import datetime

import boto3
from app.domain.exception.custom_exception import NoExistUserException
from boto3.dynamodb.conditions import Key

table_name = "pomodoro_info"


@dataclass
class Task:
    task_id: str
    name: str
    shortcut_flg: bool
    children_task_id: list[str]
    done: bool
    finished_workload: int
    estimated_workload: int
    deadline: datetime
    notes: str


def fetch_task_service(user_id: str) -> list[Task]:
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)
    task_list = table.query(KeyConditionExpression=Key("ID").eq(f"{user_id}_task"))[
        "Items"
    ]

    # rootタスクすらない場合、ユーザ登録が完了していない
    if len(task_list) == 0:
        raise NoExistUserException()

    return [_create_task(task_dict) for task_dict in task_list]


def _create_task(task_dict: dict) -> Task:
    task_info = task_dict["TaskInfo"]
    return Task(
        task_id=task_dict["DataType"],
        done=task_dict["DataValue"] == "True",
        **task_info,
    )
