from dataclasses import asdict
from typing import Optional

from app.domain.model.entity.user import User
from app.domain.repository.user_repository import UserRepository
from app.infrastructure.dynamodb.model.user_model import (UserInfoModel,
                                                          UserModel)
from app.infrastructure.dynamodb.repository.dynamo_repository import \
    DynamoRepository


class UserDynamoRepository(UserRepository, DynamoRepository):
    """DynamoDBに登録されているユーザとやり取りをするリポジトリの実装クラス"""

    def find_by_id(self, user_id: str) -> Optional[User]:
        user_dict = self._table.get_item(Key={"ID": user_id, "DataType": "user"}).get(
            "Item", None
        )
        if not user_dict:
            return None
        user_model = UserModel(
            ID=user_dict["ID"], UserInfo=UserInfoModel(**user_dict["UserInfo"])
        )
        return user_model.to_user()

    def register_user(self, user: User):
        self._put_user(user)

    def update_user(self, user: User):
        self._put_user(user)

    def _put_user(self, user: User):
        user_model = UserModel.to_model(user)
        self._table.put_item(Item=asdict(user_model))
