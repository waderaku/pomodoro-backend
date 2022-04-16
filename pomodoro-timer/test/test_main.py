import json
import subprocess
from pathlib import Path

import pytest
from dotenv import load_dotenv

TEST_PATH = Path("/").joinpath(
    "root", "workspaces", "pomodoro-backend", "pomodoro-timer", "test"
)
param_path = TEST_PATH.joinpath("param.json")
with param_path.open("r") as f:
    param: dict = json.load(f)


@pytest.fixture(scope="session", autouse=True)
def setup_container():
    subprocess.run(
        r"docker run --rm -d --name test-dynamodb -p 8001:8001 --net=pomodoro-timer amazon/dynamodb-local ",
        shell=True,
    )
    path = TEST_PATH.joinpath(".env")
    load_dotenv(path)
    yield
    subprocess.run(r"docker stop test-dynamodb", shell=True)
