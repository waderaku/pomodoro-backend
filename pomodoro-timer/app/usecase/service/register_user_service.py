from typing import Optional

import inject
from app.domain.exception.custom_exception import AlreadyExistUserException
from app.domain.model.entity.user import User
from app.domain.repository.user_repository import UserRepository


@inject.params(user_repository=UserRepository)
def register_user_service(
    user_id: str, user_repository: Optional[UserRepository] = None
):
    """新規にユーザーデータを登録する

    Args:
        user_repository (UserRepository): ユーザ情報についてDBとやり取りを行うリポジトリ
        user_id (str): ユーザーID

    Raises:
        AlreadyExistUserException: 既に対象のユーザーが存在する場合に発行される例外
    """
    # 存在チェック
    if user_repository.find_by_id(user_id=user_id):
        raise AlreadyExistUserException()

    # 新規登録
    user = User.create(user_id)
    user_repository.register_user(user=user)
