import os

import boto3
from boto3.dynamodb.conditions import Key

table_name = "pomodoro_info"


def fetch_task_service(user_id: str) -> tuple[list[dict], list[dict]]:
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
