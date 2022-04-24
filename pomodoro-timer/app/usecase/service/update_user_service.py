import os

import boto3
from app.usecase.exception.custom_exception import (
    NoExistUserException,
    NotSettingConfigException,
)

table_name = "pomodoro_info"


def update_user_service(
    user_id: str,
    is_google_linked: bool,
    default_length: dict[str, int],
    google_config: dict[str, dict] | None = None,
):
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"ID": user_id, "DataType": "user"})

    if not "Item" in response:
        raise NoExistUserException()

    user = response["Item"]
    # googleとリンクするのにconfig設定がない場合エラー
    if is_google_linked and not google_config:
        raise NotSettingConfigException()

    user_info = {"is_google_linked": is_google_linked, "default_length": default_length}
    if google_config:
        user_info["google_config"] = google_config

    user["UserInfo"].update(user_info)

    table.put_item(Item=user)
