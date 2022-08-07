from app.domain.repository.auth_user_repository import AuthUserRepository
from app.infrastructure.dynamodb.model.user_model import (UserInfoModel,
                                                          UserModel)
from app.infrastructure.dynamodb.repository.dynamo_repository import \
    DynamoRepository


class AuthUserDynamoRepository(AuthUserRepository, DynamoRepository):
    def find_by_id(self, user_id: str):
        user_dict = self._table.get_item(Key={"ID": user_id, "DataType": "user"}).get(
            "Item", None
        )
        if not user_dict:
            return None
        user_model = UserModel(
            ID=user_dict["ID"], UserInfo=UserInfoModel(**user_dict["UserInfo"])
        )
        return user_model.to_auth_user()
