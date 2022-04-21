import os
from datetime import datetime

import boto3


def register_event_service(
    user_id: str,
    task_id: str,
    start: datetime,
    end: datetime,
):
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table_name = "pomodoro_info"
