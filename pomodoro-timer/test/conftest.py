import subprocess
from pathlib import Path

import inject
import pytest
from dotenv import load_dotenv
from main import inject_config

TEST_PATH = Path("/").joinpath(
    "root", "workspaces", "pomodoro-backend", "pomodoro-timer", "test"
)


@pytest.fixture(scope="session", autouse=True)
def setup_container():
    subprocess.run(
        r"docker run --rm -d --name test-dynamodb -p 8001:8001 --net=pomodoro-timer amazon/dynamodb-local ",
        shell=True,
    )
    path = TEST_PATH.joinpath(".env")
    load_dotenv(path)
    inject.configure(inject_config)
    yield
    subprocess.run(r"docker stop test-dynamodb", shell=True)
