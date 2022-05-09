import inject
from app.domain.exception.custom_exception import NoExistUserException
from app.domain.model.entity.user import User
from app.domain.repository.user_repository import UserRepository


@inject.params(user_repository=UserRepository)
def fetch_user_service(user_repository: UserRepository, user_id: str) -> User:
    """ユーザIDに紐づくユーザ情報を取得する

    Args:
        user_repository (UserRepository): ユーザ情報についてDBとやり取りを行うリポジトリ
        user_id (str): ユーザID

    Raises:
        NoExistUserException: 対象のユーザが存在しないことを示す例外

    Returns:
        User: 取得したユーザ
    """
    user = user_repository.find_by_id(user_id=user_id)
    if not user:
        raise NoExistUserException()
    return user
