from __future__ import annotations

import secrets
from datetime import datetime, timedelta

from app.domain.model.value.auth_token import AuthToken

TOKEN_EXPIRED_DAYS = 1


class TokenUser:
    def __init__(self, user_id: str, auth_token: AuthToken):
        self._user_id = user_id
        self._auth_token = auth_token

    @classmethod
    def create(cls, user_id: str) -> TokenUser:
        return cls(
            user_id=user_id,
            auth_token=AuthToken(
                secrets.token_hex(), datetime.now() + timedelta(days=TOKEN_EXPIRED_DAYS)
            ),
        )

    def is_expired(self) -> bool:
        return self._auth_token.is_expired()
