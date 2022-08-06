from abc import ABC, abstractmethod
from typing import Optional

from app.domain.model.entity.token_user import TokenUser


class TokenUserRepository(ABC):
    @abstractmethod
    def register_token(self, token_user: TokenUser) -> TokenUser:
        """発行したトークンを追加登録する

        Args:
            token_user (str): トークンデータ
        """
        raise NotImplementedError()

    @abstractmethod
    def find_by_token(self, token: str) -> Optional[TokenUser]:
        """トークンに紐づくデータを取得する

        Args:
            token (str): トークン

        Returns:
            TokenUser: トークンデータ
        """
        raise NotImplementedError()
