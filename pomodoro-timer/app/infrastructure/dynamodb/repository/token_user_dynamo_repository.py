from dataclasses import asdict
from typing import Optional

from app.domain.model.entity.token_user import TokenUser
from app.domain.repository.token_user_repository import TokenUserRepository
from app.infrastructure.dynamodb.model.token_user_model import TokenUserModel
from app.infrastructure.dynamodb.repository.dynamo_repository import DynamoRepository
from boto3.dynamodb.conditions import Key


class TokenUserDynamoRepository(TokenUserRepository, DynamoRepository):
    def register_token(self, token_user: TokenUser):
        """発行したトークンを追加登録する

        Args:
            token_user (str): トークンデータ
        """
        token_user_model = TokenUserModel.to_model(token_user)
        self._table.put_item(Item=asdict(token_user_model))

    def find_by_token(self, token: str) -> Optional[TokenUser]:
        item_list = self._table.query(KeyConditionExpression=Key("ID").eq(token))[
            "Items"
        ]
        if len(item_list) == 0:
            return
        token_user_dict = item_list[0]
        return TokenUserModel(**token_user_dict).to_token_user()

    def delete_by_token(self, token: str):
        self._table.delete_item(Key={"ID": token, "DataType": "token"})
