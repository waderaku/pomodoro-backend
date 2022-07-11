from abc import ABC, abstractmethod

from app.domain.model.entity.task_user import TaskUser


class TaskUserRepository(ABC):
    @abstractmethod
    def register_task_user(self, task_user: TaskUser):
        """タスク、ユーザをDBに登録する

        Args:
            task_user (TaskUser): 登録するタスク、ユーザ集約
        """
        raise NotImplementedError()
