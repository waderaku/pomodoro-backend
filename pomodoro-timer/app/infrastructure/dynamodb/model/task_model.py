from __future__ import annotations

from dataclasses import dataclass

from app.domain.model.entity.task import Task


@dataclass
class TaskInfoModel:
    name: str
    shortcut_flg: bool
    children_task_id: list[str]
    finished_workload: int
    estimated_workload: int
    deadline: str
    notes: str


@dataclass
class TaskModel:
    ID: str
    DataType: str
    DataValue: str
    TaskInfo: TaskInfoModel

    @classmethod
    def to_model(cls, task: Task) -> TaskModel:
        """ドメインのユーザオブジェクトをDBに登録する形式に変換する

        Args:
            task (Task): ユーザオブジェクト
        """
        task_info_model = TaskInfoModel(
            name=task._name,
            shortcut_flg=task._shortcut_flg,
            children_task_id=task._children_task_id,
            finished_workload=task._finished_workload,
            estimated_workload=task._estimated_workload,
            deadline=task._deadline,
            notes=task._notes,
        )
        return cls(
            ID=f"{task._user_id}_task",
            DataType=task._task_id,
            DataValue="True" if task._done else "False",
            TaskInfo=task_info_model,
        )
