from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from app.domain.model.entity.user import User
from app.domain.model.value.default_length import DefaultLength
from app.domain.model.value.google_config import Calendar, GoogleConfig, TaskList


@dataclass
class UserInfoModel:
    is_google_linked: bool
    default_length: dict
    google_config: Optional[dict] = None
    password: Optional[str] = None


@dataclass
class UserModel:
    ID: str
    UserInfo: UserInfoModel
    DataType: str = "user"

    def to_user(self) -> User:
        """ドメインのユーザオブジェクトに変換する

        Returns:
            User: 変換したユーザオブジェクト
        """
        user_info = self.UserInfo
        default_length = DefaultLength(
            work=int(user_info.default_length["work"]),
            rest=int(user_info.default_length["rest"]),
        )

        google_config = None
        if user_info.google_config:
            google_config = GoogleConfig(
                Calendar(**user_info.google_config["calendar"]),
                TaskList(**user_info.google_config["task_list"]),
            )
        return User(
            user_id=self.ID,
            is_google_linked=user_info.is_google_linked,
            default_length=default_length,
            google_config=google_config,
            password=self.UserInfo.password,
        )

    @classmethod
    def to_model(cls, user: User) -> UserModel:
        """ドメインのユーザオブジェクトをDBに登録する形式に変換する

        Args:
            user (User): ユーザオブジェクト
        """
        user_info_model = UserInfoModel(
            is_google_linked=user._is_google_linked,
            google_config=None
            if not user._google_config
            else asdict(user._google_config),
            default_length=asdict(user._default_length),
            password=user._password,
        )
        return cls(ID=user._user_id, UserInfo=user_info_model)
