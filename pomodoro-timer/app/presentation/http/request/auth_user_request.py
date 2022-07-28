from datetime import datetime

from pydantic import BaseModel


class AuthUser(BaseModel):
    """認証用のユーザデータクラス
    一時的に作成しているが、Cognito連携時に削除
    """

    userId: str
    password: str
