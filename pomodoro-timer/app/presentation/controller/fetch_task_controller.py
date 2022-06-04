import os

import boto3
from app.presentation.http.response.task_response import Task, TaskData, TaskResponse
from boto3.dynamodb.conditions import Key
from fastapi import Header

table_name = "pomodoro_info"


async def fetch_task(userId: str = Header(None)) -> list[TaskResponse]:
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)
    task_list = table.query(KeyConditionExpression=Key("ID").eq(f"{userId}_task"))[
        "Items"
    ]
    root_task_list = table.query(
        IndexName="dataValueLSIndex",
        KeyConditionExpression=Key("ID").eq(userId) & Key("DataValue").eq("root_task"),
    )["Items"]
    response_task_list = [_create_task(task) for task in task_list]
    response_root_id = [root_task["DataType"][:-5] for root_task in root_task_list]
    return TaskResponse(task=response_task_list, rootTaskId=response_root_id)


def _create_task(task: dict):
    task_data_dict = task["TaskInfo"]
    task_data = TaskData(
        name=task_data_dict["name"],
        childrenIdList=task_data_dict["children_task_id"],
        done=task["DataValue"],
        finishedWorkload=task_data_dict["finished_workload"],
        estimatedWorkload=task_data_dict["estimated_workload"],
        deadline=task_data_dict["deadline"],
        notes=task_data_dict["notes"],
    )
    return Task(id=task["DataType"], taskData=task_data)
