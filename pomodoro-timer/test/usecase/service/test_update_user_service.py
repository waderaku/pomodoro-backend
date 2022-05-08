import json
from decimal import Decimal
from pathlib import Path
from test.common import initial_process
from test.db_util import clear_and_insert, fetch_user

import pytest
from app.usecase.service.update_user_service import update_user_service

TEST_PATH = Path("/").joinpath(
    "root",
    "workspaces",
    "pomodoro-backend",
    "pomodoro-timer",
    "test",
    "usecase",
    "service",
)
test_data_success_path = TEST_PATH.joinpath("test_update_user_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = TEST_PATH.joinpath("test_update_user_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########ユーザー登録正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_update_user_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    update_user_service(**request)
    user = fetch_user(request["user_id"])
    assert answer == user


##########ユーザー登録異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_update_user_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        update_user_service(**request)
    assert str(e.value) == answer["error_message"]
