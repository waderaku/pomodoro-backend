from __future__ import annotations

import hashlib
from typing import Optional

from app.domain.exception.custom_exception import NotSettingConfigException
from app.domain.model.value.default_length import DefaultLength
from app.domain.model.value.google_config import GoogleConfig
from app.domain.model.value.password import Password


class User:
    def __init__(
        self,
        user_id: str,
        is_google_linked: bool,
        default_length: DefaultLength,
        google_config: Optional[GoogleConfig],
        password: Optional[Password] = None,
    ):
        self._user_id = user_id
        self._password = password
        self._is_google_linked = is_google_linked
        self._default_length = default_length
        self._google_config = google_config

    @classmethod
    def create(cls, user_id: str, plain_password: str) -> User:
        """ユーザオブジェクトの新規作成をする.
        初期のタイマー設定時間は作業時間が25分、休憩時間が5分とする
        Googleとの連携はない状態とする

        Args:
            user_id (str): 新規作成するユーザのID
            plain_password(str): 新規作成するユーザのパスワード、Cognito連携時に削除

        Returns:
            User:新規作成されたユーザオブジェクト
        """
        hashed_password = Password(value=plain_password, is_hashed=False)

        return cls(
            user_id=user_id,
            password=hashed_password,
            is_google_linked=False,
            default_length=DefaultLength(25, 5),
            google_config=None,
        )

    def update(
        self,
        is_google_linked: bool,
        default_length: DefaultLength,
        google_config: Optional[GoogleConfig],
    ):
        """ユーザオブジェクトの更新をする.
        Googleとリンクする場合、必ずgoogle_configの設定が必要とする

        Args:
            is_google_linked (bool): Googleサイトとのリンク設定
            default_length (DefaultLength): 作業、休憩時間の基本設定
            google_config (Optional[GoogleConfig]): Google連携する際のカレンダーやタスクのID

        Raises:
            NotSettingConfigException: カレンダーやタスクリストの指定がない状態でGoogle連携しようとしていることを示す例外
        """

        if is_google_linked and not google_config:
            raise NotSettingConfigException()

        self._is_google_linked = is_google_linked
        self._default_length = default_length
        self._google_config = google_config

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, User):
            return False
        return (
            self._user_id == o._user_id
            and self._is_google_linked == o._is_google_linked
            and self._default_length == o._default_length
            and self._google_config == o._google_config
        )
