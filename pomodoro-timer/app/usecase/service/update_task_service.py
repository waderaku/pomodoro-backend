import os
from dataclasses import dataclass
from datetime import datetime

import boto3
from app.domain.exception.custom_exception import NoExistTaskException
from boto3.dynamodb.conditions import Key

table_name = "pomodoro_info"


def update_task_service(
    user_id: str,
    task_id: str,
    name: str,
    estimated_workload: int,
    deadline: datetime,
    notes: str,
    done: bool,
    shortcut_flg: bool,
):

    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)

    # タスク一覧の取得
    task_list: list[dict] = table.query(
        KeyConditionExpression=Key("ID").eq(f"{user_id}_task")
    )["Items"]

    update_task_list = []

    # タスク一覧からツリーを展開
    task_dict = _create_task_dict(task_list)
    update_task: dict = task_dict.get(task_id)
    # 更新対象のタスクが存在しない場合はエラー
    if not update_task:
        raise NoExistTaskException()

    # タスクデータの更新
    update_task.update(
        {
            "ID": f"{user_id}_task",
            "DataType": task_id,
            "DataValue": "True" if done else "False",
        }
    )
    update_task["TaskInfo"].update(
        {
            "name": name,
            "estimated_workload": estimated_workload,
            "deadline": deadline.strftime("%Y-%m-%d"),
            "notes": notes,
            "shortcut_flg": shortcut_flg,
        }
    )
    update_task_name = {"ID": user_id, "DataType": f"{task_id}_name", "DataValue": name}
    update_task_deadline = {
        "ID": user_id,
        "DataType": f"{task_id}_deadline",
        "DataValue": deadline.strftime("%Y-%m-%d"),
    }

    # ツリーから親子タスクの更新
    task_tree = _create_root_tree(task_list)
    update_task_list = _update_task_tree(task_dict, task_tree, update_task, user_id)

    with table.batch_writer() as batch:
        for task in update_task_list:
            batch.put_item(Item=task)
        batch.put_item(update_task_name)
        batch.put_item(update_task_deadline)


def _update_task_tree(
    task_dict: dict, task_tree: dict, update_task: dict, user_id: str
) -> list[dict]:

    update_deadline = update_task["TaskInfo"]["deadline"]
    update_deadline_flg = True
    update_estimated_workload = update_task["TaskInfo"]["estimated_workload"]
    update_estimated_workload_flg = True
    update_done_flg = update_task["DataValue"] == "False"
    target_task = task_tree.get(update_task["DataType"])
    update_task_list = [update_task]

    # 親タスク方向に更新
    while True:
        if not target_task:
            break

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
                update_estimated_workload_flg = False

        # 子タスクがFalseに変更された場合、親タスクもFalseにする
        if update_done_flg:
            if target_task["DataValue"] == "True":
                target_task["DataValue"] = "False"
            else:
                update_done_flg = False

        # 見積もり時間、日付、タスク完了フラグ全てが更新不要になったら終了
        if (
            not update_deadline_flg
            and not update_estimated_workload_flg
            and not update_done_flg
        ):
            break

        update_task_list.append(target_task)

        # 対象を一つ親のタスクに変更
        target_task = task_tree.get(target_task["DataType"])

    # 子タスク方向に更新
    if update_task["DataValue"] == "True":
        _update_children_task(task_dict, update_task, update_task_list)

    return update_task_list


def _update_children_task(task_dict, update_task, update_task_list):
    for child_task_id in update_task["TaskInfo"]["children_task_id"]:
        child_task = task_dict[child_task_id]
        if child_task["DataValue"] == "False":
            child_task["DataValue"] = "True"
            update_task_list.append(child_task)
            _update_children_task(task_dict, child_task, update_task_list)


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
