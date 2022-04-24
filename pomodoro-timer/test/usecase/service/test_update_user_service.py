import json
from decimal import Decimal
from pathlib import Path
from test.db_util import clear_and_insert, fetch_user

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
test_data_success_path = TEST_PATH.joinpath("test_update_user_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = TEST_PATH.joinpath("test_update_user_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########ユーザー登録正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_register_event_success_task(test_data_success: dict):
    request = test_data_success["request"]
    answer = test_data_success["answer"]
    db_data = test_data_success["db"]
    clear_and_insert(db_data)

    register_user_service(**request)
    user = fetch_user(request["user_id"])
    assert answer == user


##########ユーザー登録異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_register_event_failed_task(test_data_failed: dict):
    request = test_data_failed["request"]
    answer = test_data_failed["answer"]
    db_data = test_data_failed["db"]
    clear_and_insert(db_data)

    with pytest.raises(Exception) as e:
        register_user_service(**request)
    assert str(e.value) == answer["error_message"]
