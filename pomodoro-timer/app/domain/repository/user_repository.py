from abc import ABC, abstractmethod
from typing import Optional

from app.domain.model.entity.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        """ユーザIDに紐づくユーザを取得する.
        対象のユーザが存在しない場合、nullを返却する

        Args:
            user_id (str): ユーザID

        Returns:
            Optional[User]: 取得したユーザ
        """
        raise NotImplementedError()

    @abstractmethod
    def register_user(self, user: User):
        """ユーザをDBに登録する

        Args:
            user (User): 登録するユーザ
        """
        raise NotImplementedError()

    @abstractmethod
    def update_user(self, user: User):
        """登録されているユーザを更新する

        Args:
            user (User): 更新するユーザ
        """
        raise NotImplementedError()
