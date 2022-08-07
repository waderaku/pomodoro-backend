from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuthToken:
    value: str
    deadline: datetime

    def is_valid(self, token: str) -> bool:
        return self.value == token and datetime.now() < self.deadline
