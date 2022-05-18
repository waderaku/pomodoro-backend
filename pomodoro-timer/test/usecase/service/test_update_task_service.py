import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from test.common import initial_process
from test.db_util import fetch_deadline_task, fetch_task

import pytest
from app.usecase.service.update_task_service import update_task_service

TEST_PATH = Path("/").joinpath(
    "root",
    "workspaces",
    "pomodoro-backend",
    "pomodoro-timer",
    "test",
    "usecase",
    "service",
)
test_data_success_path = TEST_PATH.joinpath("test_update_task_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = TEST_PATH.joinpath("test_update_task_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########タスク更新正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list[:2])
def test_update_task_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    request["deadline"] = datetime.strptime(request["deadline"], "%Y-%m-%d")
    update_task_service(**request)

    task_list = fetch_task(request["user_id"])

    assert answer == task_list


@pytest.mark.parametrize("test_data_success", test_data_success_list[2])
def test_update_for_parent_task_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    request["deadline"] = datetime.strptime(request["deadline"], "%Y-%m-%d")
    update_task_service(**request)

    task_list = fetch_task(request["user_id"])
    deadline_list = [
        fetch_deadline_task(request["user_id"], task["DataType"]) for task in task_list
    ]
    assert answer["task_list"] == task_list
    assert answer["deadline_list"] == deadline_list


##########ユーザー登録異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_update_task_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        update_task_service(**request)
    assert str(e.value) == answer["error_message"]
