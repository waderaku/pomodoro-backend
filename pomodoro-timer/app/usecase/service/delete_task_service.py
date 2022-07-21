import os
from turtle import xcor

import boto3
from app.domain.exception.custom_exception import (DeleteRootTaskException,
                                                   NoExistTaskException,
                                                   NoExistUserException)
from boto3.dynamodb.conditions import Key

table_name = "pomodoro_info"


def delete_task_service(user_id: str, task_id: str):

    if task_id == "root":
        raise DeleteRootTaskException()

    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)
    task_list = table.query(KeyConditionExpression=Key("ID").eq(f"{user_id}_task"))[
        "Items"
    ]

    if len(task_list) == 0:
        raise NoExistUserException()

    if not next(filter(lambda x: x["DataType"] == task_id, task_list), None):
        raise NoExistTaskException()

    event_list = table.query(KeyConditionExpression=Key("ID").eq(f"{user_id}_event"))[
        "Items"
    ]
    delete_task_list = get_delete_task(task_list, task_id)

    update_event_list = get_update_event(
        event_list, task_list, delete_task_list, task_id
    )
    with table.batch_writer() as batch:
        for delete_task in delete_task_list:
            batch.delete_item(
                Key={"ID": delete_task["ID"], "DataType": delete_task["DataType"]}
            )

        for update_event in update_event_list:
            batch.put_item(Item=update_event)


def get_update_event(
    event_list: list[dict],
    task_list: list[dict],
    delete_task_list: list[dict],
    task_id: str,
) -> list[dict]:
    parent_task = None
    for task in task_list:
        if task_id in task["TaskInfo"]["children_task_id"]:
            parent_task = task
            break

    delete_task_id_list = [delete_task["DataType"] for delete_task in delete_task_list]

    update_event_list = [
        {**event, "DataValue": parent_task["DataType"]}
        for event in event_list
        if event["DataValue"] in delete_task_id_list
    ]
    return update_event_list


def get_delete_task(task_list: list[dict], delete_task_id: str) -> list[dict]:
    task_dict = _create_task_dict(task_list)
    delete_task_list = []
    _add_delete_task(task_dict, delete_task_id, delete_task_list)
    return delete_task_list


def _add_delete_task(
    task_dict: dict, delete_task_id: str, delete_task_list: list[dict]
):
    delete_task = task_dict[delete_task_id]
    delete_task_list.append(delete_task)
    children_task_id_list = delete_task["TaskInfo"]["children_task_id"]
    if len(children_task_id_list) == 0:
        return
    for child_task in children_task_id_list:
        _add_delete_task(task_dict, child_task, delete_task_list)


def _create_task_dict(task_list: list[dict]) -> dict:
    task_dict = {task["DataType"]: task for task in task_list}
    return task_dict
