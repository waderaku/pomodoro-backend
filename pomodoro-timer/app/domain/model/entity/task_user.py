from __future__ import annotations

from app.domain.model.entity.task import Task
from app.domain.model.entity.user import User


class TaskUser:
    def __init__(self, user: User, task_list: list[Task]):
        self._user = user
        self._task_list = task_list

    @classmethod
    def create(
        cls,
        user_id: str,
    ) -> TaskUser:
        """ユーザオブジェクトの新規作成をする.
        初期のタイマー設定時間は作業時間が25分、休憩時間が5分とする
        Googleとの連携はない状態とする

        Args:
            user_id (str): 新規作成するユーザのID

        Returns:
            User:新規作成されたユーザオブジェクト
        """
        task = Task.create_root(user_id=user_id)
        user = User.create(user_id=user_id)
        task_user = cls(
            user=user,
            task_list=[task],
        )
        return task_user
