from dataclasses import asdict

from app.domain.model.entity.token_user import TokenUser
from app.domain.repository.token_user_repository import TokenUserRepository
from app.infrastructure.dynamodb.model.token_user_model import TokenUserModel
from app.infrastructure.dynamodb.repository.dynamo_repository import DynamoRepository


class TokenUserDynamoRepository(TokenUserRepository, DynamoRepository):
    def register_token(self, token_user: TokenUser):
        """発行したトークンを追加登録する

        Args:
            token_user (str): トークンデータ
        """
        token_user_model = TokenUserModel.to_model(token_user)
        self._table.put_item(Item=asdict(token_user_model))
