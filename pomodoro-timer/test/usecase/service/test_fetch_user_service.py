import json
from decimal import Decimal
from pathlib import Path
from test.common import initial_process

import pytest
from app.domain.model.entity.user import User
from app.domain.model.value.default_length import DefaultLength
from app.domain.model.value.google_config import (Calendar, GoogleConfig,
                                                  TaskList)
from app.usecase.service.fetch_user_service import fetch_user_service

TEST_PATH = Path("/").joinpath(
    "root",
    "workspaces",
    "pomodoro-backend",
    "pomodoro-timer",
    "test",
    "usecase",
    "service",
)
test_data_success_path = TEST_PATH.joinpath("test_fetch_user_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = TEST_PATH.joinpath("test_fetch_user_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########ユーザー取得正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_fetch_user_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    user = fetch_user_service(**request)
    answer_user = User(
        user_id=answer["user_id"],
        is_google_linked=answer["is_google_linked"],
        default_length=DefaultLength(**answer["default_length"]),
        google_config=None
        if not answer["google_config"]
        else GoogleConfig(
            Calendar(**answer["google_config"]["calendar"]),
            TaskList(**answer["google_config"]["task_list"]),
        ),
    )

    assert answer_user == user


##########ユーザー取得異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_fetch_user_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        user = fetch_user_service(**request)
    assert str(e.value) == answer["error_message"]
