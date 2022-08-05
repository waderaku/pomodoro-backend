from abc import ABC, abstractmethod

from app.domain.model.entity.token_user import TokenUser


class TokenUserRepository(ABC):
    @abstractmethod
    def register_token(self, token_user: TokenUser) -> TokenUser:
        """発行したトークンを追加登録する

        Args:
            token_user (str): トークンデータ
        """
        raise NotImplementedError()
