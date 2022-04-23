import os

import boto3
from boto3.dynamodb.conditions import Key
from create_table import create_table

TABLE_NAME = "pomodoro_info"


def clear_and_insert(db: list[dict]):
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    if TABLE_NAME in [tbl.name for tbl in dynamodb.tables.all()]:
        dynamodb.Table(TABLE_NAME).delete()

    table = create_table()

    with table.batch_writer() as batch:
        for db_data in db:
            batch.put_item(Item=db_data)


def fetch_task(user_id: str) -> list[dict]:
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(TABLE_NAME)
    return table.query(KeyConditionExpression=Key("ID").eq(f"{user_id}_task"))["Items"]


def fetch_event(user_id: str) -> list[dict]:
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table = dynamodb.Table(TABLE_NAME)
    return table.query(KeyConditionExpression=Key("ID").eq(f"{user_id}_event"))["Items"]
