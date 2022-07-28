from typing import Optional

import inject
from app.domain.exception.custom_exception import AlreadyExistUserException
from app.domain.model.entity.task_user import TaskUser
from app.domain.repository.task_user_repository import TaskUserRepository
from app.domain.repository.user_repository import UserRepository


@inject.params(task_user_repository=TaskUserRepository, user_repository=UserRepository)
def register_user_service(
    user_id: str,
    password: str,
    task_user_repository: Optional[TaskUserRepository] = None,
    user_repository: Optional[UserRepository] = None,
):
    """新規にユーザーデータを登録する

    Args:
        user_id (str): ユーザーID
        password(str): パスワード、Cognito連携時に削除

    Raises:
        AlreadyExistUserException: 既に対象のユーザーが存在する場合に発行される例外
    """
    # 存在チェック
    if user_repository.find_by_id(user_id=user_id):
        raise AlreadyExistUserException()

    # 新規登録
    task_user = TaskUser.create(user_id, password=password)
    task_user_repository.register_task_user(task_user=task_user)
