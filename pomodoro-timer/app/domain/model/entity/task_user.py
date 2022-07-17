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
        それに伴い、当該ユーザに紐づくrootタスクを作成する

        Args:
            user_id (str): 新規作成するユーザのID

        Returns:
            TaskUser:新規作成されたユーザ、タスクの集約オブジェクト
        """
        task = Task.create_root(user_id=user_id)
        user = User.create(user_id=user_id)
        task_user = cls(
            user=user,
            task_list=[task],
        )
        return task_user
