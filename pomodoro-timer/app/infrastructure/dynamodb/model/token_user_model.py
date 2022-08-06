from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.model.entity.token_user import TokenUser
from app.domain.model.value.auth_token import AuthToken


@dataclass
class TokenUserModel:
    ID: str
    DataType: str
    DataValue: str
    Deadline: str

    @classmethod
    def to_model(cls, token_user: TokenUser) -> TokenUserModel:
        return cls(
            ID=token_user._auth_token.value,
            DataType=token_user._user_id,
            DataValue="token",
            Deadline=token_user._auth_token.deadline.isoformat(),
        )

    def to_token_user(self) -> TokenUser:
        auth_token = AuthToken(self.ID, datetime.fromisoformat(self.Deadline))
        return TokenUser(self.DataType, auth_token)
