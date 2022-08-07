from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from app.domain.exception.custom_exception import PasswordIsInvalidException

# パスワードは大文字小文字含む英数字8文字以上24文字以内
REGIX = "\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[a-zA-Z\d]{8,24}\Z"


@dataclass
class Password:
    value: str
    is_hashed: bool

    def __post_init__(self):
        if self.is_hashed:
            return

        if not self.valid():
            raise PasswordIsInvalidException()

        # パスワードのハッシュ化
        self.value = hashlib.sha256(self.value.encode()).hexdigest()
        self.is_hashed = True

    def valid(self) -> bool:
        return bool(re.match(REGIX, self.value))

    def __eq__(self, o: Password) -> bool:
        return self.value == o.value
