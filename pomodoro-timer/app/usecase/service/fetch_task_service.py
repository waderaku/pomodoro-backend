import os
from dataclasses import dataclass
from datetime import datetime

import boto3
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


def fetch_task_service(user_id: str) -> Task:
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)
    task_list = table.query(KeyConditionExpression=Key("ID").eq(f"{user_id}_task"))[
        "Items"
    ]
    root_task_list = table.query(
        IndexName="dataValueLSIndex",
        KeyConditionExpression=Key("ID").eq(user_id) & Key("DataValue").eq("root_task"),
    )["Items"]
    return task_list, root_task_list
