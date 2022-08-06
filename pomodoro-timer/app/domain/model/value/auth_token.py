from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuthToken:
    value: str
    deadline: datetime

    def is_expired(self) -> bool:
        """このトークンが有効期限切れかを示す。
        Trueなら有効期限切れのため、使用できない

        Returns:
            bool: 有効期限切れの場合True
        """
        return datetime.now() > self.deadline
