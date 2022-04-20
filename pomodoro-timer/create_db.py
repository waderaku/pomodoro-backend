import os
import boto3
from dotenv import load_dotenv

def create_db():
    resource = boto3.resource(
        "dynamodb",
        endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None),
    )
    table_name = "pomodoro_info"
    resource.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {"AttributeName": "ID", "AttributeType": "S"},
            {"AttributeName": "DataType", "AttributeType": "S"},
            {"AttributeName": "DataValue", "AttributeType": "S"}
        ],
        KeySchema=[
            {"AttributeName": "ID", "KeyType": "HASH"},
            {"AttributeName": "DataType", "KeyType": "RANGE"},
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'dataValueLSIndex',
                'KeySchema': [
                    {'AttributeName': 'ID','KeyType': 'HASH'},
                    {'AttributeName': 'DataValue','KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'}
            },
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )


if __name__ == "__main__":
    load_dotenv("/root/workspaces/pomodoro-backend/pomodoro-timer/app/.env")
    create_db()
