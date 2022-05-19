import os
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import boto3
from app.domain.exception.custom_exception import (
    AlreadyDoneParentTaskException,
    NoExistParentTaskException,
    NoExistUserException,
)
from boto3.dynamodb.conditions import Key

table_name = "pomodoro_info"


@dataclass
class Task:
    task_id: str


def register_task_service(
    user_id: str,
    parent_id: str,
    name: str,
    estimated_workload: int,
    deadline: datetime,
    notes: str,
):

    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)

    # 対象ユーザーの存在確認
    if not table.get_item(Key={"ID": user_id, "DataType": "user"}).get("Item"):
        raise NoExistUserException()

    # タスク一覧の取得
    task_list: list[dict] = table.query(
        KeyConditionExpression=Key("ID").eq(f"{user_id}_task")
    )["Items"]

    # 新規追加タスクの作成
    additional_task_id = str(uuid4())
    root_flg = parent_id == ""
    additional_task = {
        "ID": f"{user_id}_task",
        "DataType": additional_task_id,
        "DataValue": "False",
        "TaskInfo": {
            "name": name,
            "children_task_id": [],
            "finished_workload": Decimal("0.0"),
            "estimated_workload": estimated_workload,
            "deadline": deadline.strftime("%Y-%m-%d"),
            "notes": notes,
        },
    }
    additional_task_deadline = {
        "ID": user_id,
        "DataType": f"{additional_task_id}_deadline",
        "DataValue": deadline.strftime("%Y-%m-%d"),
    }
    additional_task_name = {
        "ID": user_id,
        "DataType": f"{additional_task_id}_name",
        "DataValue": name,
    }
    additional_task_root_flg = {
        "ID": user_id,
        "DataType": f"{additional_task_id}_root",
        "DataValue": "root_task",
    }
    task_list.append(additional_task)

    update_task_list = []
    if not root_flg:
        # 親タスクに子タスク情報を追加
        parent_task_list = list(filter(lambda x: x["DataType"] == parent_id, task_list))
        if len(parent_task_list) == 0:
            raise NoExistParentTaskException()
        parent_task = parent_task_list[0]
        if parent_task["DataValue"] == "True":
            raise AlreadyDoneParentTaskException()

        parent_task["TaskInfo"]["children_task_id"].append(additional_task_id)

        # 新規タスク一覧からツリーを展開
        task_dict = _create_task_dict(task_list)
        task_tree = _create_root_tree(task_list)

        # そのツリーから元々のタスクの更新
        update_task_list = _update_task_tree(
            task_dict, task_tree, additional_task, user_id
        )

    with table.batch_writer() as batch:
        for task in update_task_list:
            batch.put_item(Item=task)
        batch.put_item(Item=additional_task)
        batch.put_item(Item=additional_task_deadline)
        batch.put_item(Item=additional_task_name)
        if root_flg:
            batch.put_item(Item=additional_task_root_flg)

    return Task(additional_task_id)


def _update_task_tree(
    task_dict: dict, task_tree: dict, additional_task: dict, user_id: str
) -> list[dict]:

    update_deadline = additional_task["TaskInfo"]["deadline"]
    update_deadline_flg = True
    update_estimated_workload = additional_task["TaskInfo"]["estimated_workload"]
    update_estimated_workload_flg = True
    target_task = task_tree[additional_task["DataType"]]
    update_task_list = []
    while True:
        # 日付更新
        if update_deadline_flg:
            target_deadline = target_task["TaskInfo"]["deadline"]
            if target_deadline < update_deadline:
                target_task["TaskInfo"]["deadline"] = update_deadline
                update_task_list.append(
                    {
                        "ID": user_id,
                        "DataType": f"{target_task['DataType']}_deadline",
                        "DataValue": update_deadline,
                    }
                )
            else:
                update_deadline_flg = False
        # 見積もり時間の更新
        if update_estimated_workload_flg:
            target_estimated_workload = target_task["TaskInfo"]["estimated_workload"]
            sum_children_estimated_workload = _sum_children_estimated_workload(
                task_dict, target_task
            )
            if target_estimated_workload < sum_children_estimated_workload:
                target_task["TaskInfo"][
                    "estimated_workload"
                ] = sum_children_estimated_workload
            else:
                update_estimated_workload

        # 見積もり時間も日付も更新不要になったら終了
        if not update_deadline_flg and not update_estimated_workload_flg:
            break

        update_task_list.append(target_task)

        # 対象を一つ親のタスクに変更
        target_task = task_tree.get(target_task["DataType"])
        if not target_task:
            break

    return update_task_list


def _sum_children_estimated_workload(task_dict: dict, target_task: dict):
    chldren_task_list = [
        task_dict[child_id] for child_id in target_task["TaskInfo"]["children_task_id"]
    ]

    return sum(
        [
            child_task["TaskInfo"]["estimated_workload"]
            for child_task in chldren_task_list
        ]
    )


def _create_root_tree(task_list: list[dict]) -> dict:
    root_dict = {}

    for task in task_list:
        children_id_list = task["TaskInfo"]["children_task_id"]
        for child_id in children_id_list:
            root_dict[child_id] = task

    return root_dict


def _create_task_dict(task_list: list[dict]) -> dict:
    task_dict = {task["DataType"]: task for task in task_list}
    return task_dict
