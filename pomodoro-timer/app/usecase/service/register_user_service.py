import os

import boto3
from app.usecase.exception.custom_exception import AlreadyExistUserException

table_name = "pomodoro_info"


def register_user_service(user_id: str):
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"ID": user_id, "DataType": "user"})

    if "Item" in response:
        raise AlreadyExistUserException()

    user = {
        "ID": user_id,
        "DataType": "user",
        "UserInfo": {
            "is_google_linked": False,
            "default_length": {"work": 25, "rest": 5},
        },
    }
    table.put_item(Item=user)
