import os

import boto3


def cretae_table():
    pass


def clear_and_insert(db: list[dict]):
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None)
    )
    table_name = "pomodoro-timer"
    if table_name in [tbl.name for tbl in dynamodb.tables.all()]:
        dynamodb
    dynamodb.table(table_name).delete()

    table = cretae_table()

    with table.batch_writer() as batch:
        for db_data in db:
            batch.put_item(Item=db_data)
