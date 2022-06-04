import os
from typing import Any

import boto3

TABLE_NAME = "pomodoro_info"


def get_pomodoro_table() -> Any:
    """pomodoro-infoテーブルへアクセスするboto3テーブルオブジェクトを生成する

    Returns:
        Any: 生成したboto3テーブルオブジェクト
    """
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(TABLE_NAME)
    return table
