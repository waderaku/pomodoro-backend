from abc import ABC, abstractmethod

from app.domain.model.entity.auth_user import AuthUser


class AuthUserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> AuthUser:
        """認証ユーザデータを取得する

        Args:
            user_id (str): ユーザID
        """
        raise NotImplementedError()
