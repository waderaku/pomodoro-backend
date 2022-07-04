import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from test.common import initial_process
from test.db_util import fetch_event, fetch_task

import pytest
from app.usecase.service.fetch_task_service import fetch_task_service

TEST_PATH = Path("/").joinpath(
    "root",
    "workspaces",
    "pomodoro-backend",
    "pomodoro-timer",
    "test",
    "usecase",
    "service",
)
test_data_success_path = TEST_PATH.joinpath("test_fetch_task_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


# test_data_failed_path = TEST_PATH.joinpath("test_register_task_service_failed.json")
# with test_data_failed_path.open("r") as f:
#     test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########タスク取得正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_register_task_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    task_list, root_task_list = fetch_task_service(**request)

    assert answer["task_list"] == task_list
    assert answer["root_task_list"] == root_task_list


##########タスク取得異常系テスト##############
# @pytest.mark.parametrize("test_data_failed", test_data_failed_list)
# def test_register_event_failed(test_data_failed: dict):
#     request, answer = initial_process(test_data_failed)
#     with pytest.raises(Exception) as e:
#         fetch_task_service(**request)
#     assert str(e.value) == answer["error_message"]
