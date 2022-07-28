import hashlib
import json
from decimal import Decimal
from pathlib import Path
from test.common import initial_process
from test.db_util import clear_and_insert, fetch_task, fetch_user

import pytest
from app.usecase.service.register_user_service import register_user_service

TEST_PATH = Path("/").joinpath(
    "root",
    "workspaces",
    "pomodoro-backend",
    "pomodoro-timer",
    "test",
    "usecase",
    "service",
)
test_data_success_path = TEST_PATH.joinpath("test_register_user_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = TEST_PATH.joinpath("test_register_user_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########ユーザー登録正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_register_event_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    register_user_service(**request)
    user = fetch_user(request["user_id"])
    task_list = fetch_task(request["user_id"])
    # passwordハッシュ化
    answer[0]["UserInfo"]["password"] = hashlib.sha256(
        answer[0]["UserInfo"]["password"].encode()
    ).hexdigest()
    assert answer[0] == user
    assert answer[1:] == task_list


##########ユーザー登録異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_register_event_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        register_user_service(**request)
    assert str(e.value) == answer["error_message"]
