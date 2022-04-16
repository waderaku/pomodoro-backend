import json
from pathlib import Path
from test.db_util import clear_and_insert

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

TEST_PATH = Path("/").joinpath(
    "root", "workspaces", "pomodoro-backend", "pomodoro-timer", "test"
)
test_data_path = TEST_PATH.joinpath("test_fetch_data.json")
with test_data_path.open("r") as f:
    test_data_list: list = json.load(f)

##########タスク一覧取得テスト##############
@pytest.mark.parametrize("test_data", test_data_list)
def test_fetch_root_task(test_data: dict):
    request = test_data["request"]
    answer = test_data["answer"]
    db_data = test_data["db"]
    clear_and_insert(db_data)
    response = client.get("/task", **request)
    assert response.status_code == 200
    assert response.json() == answer
