from typing import Optional

import inject
from app.domain.exception.custom_exception import NoExistUserException
from app.domain.model.value.default_length import DefaultLength
from app.domain.model.value.google_config import (Calendar, GoogleConfig,
                                                  TaskList)
from app.domain.repository.user_repository import UserRepository


@inject.params(user_repository=UserRepository)
def update_user_service(
    user_repository: UserRepository,
    user_id: str,
    is_google_linked: bool,
    default_length: dict[str, int],
    google_config: Optional[dict[str, dict]] = None,
):
    """ユーザ情報の更新を行う

    Args:
        user_repository (UserRepository): ユーザ情報についてDBとやり取りを行うリポジトリ
        user_id (str): ユーザID
        is_google_linked (bool): Googleアカウントと連携する場合True、しない場合False
        default_length (dict[str, int]): 作業時間、休憩時間の基本設定
        google_config (Optional[dict[str, dict]], optional): Googleアカウントと連携する場合のGoogleカレンダー、タスクのID

    Raises:
        NoExistUserException: 更新対象のユーザが存在しないことを示す例外
    """
    # 存在チェック
    user = user_repository.find_by_id(user_id=user_id)
    if not user:
        raise NoExistUserException()

    # ユーザの更新
    default_length = DefaultLength(default_length["work"], default_length["rest"])
    if google_config:
        google_config = GoogleConfig(
            Calendar(**google_config["calendar"]),
            TaskList(**google_config["task_list"]),
        )
    user.update(
        is_google_linked=is_google_linked,
        default_length=default_length,
        google_config=google_config,
    )
    user_repository.update_user(user)
