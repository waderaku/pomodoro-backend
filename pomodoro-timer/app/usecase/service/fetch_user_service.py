import os
from dataclasses import dataclass

import boto3
from app.usecase.exception.custom_exception import NoExistUserException

table_name = "pomodoro_info"


@dataclass
class User:
    user_id: str
    is_google_linked: bool
    default_length: dict
    google_config: dict | None


def fetch_user_service(user_id: str) -> User:
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)
    user = table.get_item(Key={"ID": user_id, "DataType": "user"}).get("Item", None)
    if not user:
        raise NoExistUserException()
    user_info = user["UserInfo"]
    return User(
        user_id=user_id,
        is_google_linked=user_info["is_google_linked"],
        default_length=user_info["default_length"],
        google_config=user_info["google_config"]
        if user_info["is_google_linked"]
        else None,
    )
