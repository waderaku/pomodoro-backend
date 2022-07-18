from __future__ import annotations

from datetime import datetime


ROOT_TASK_ID = "root"
ROOT_TASK_NAME = "HOME"
ROOT_TASK_WORKLOAD = 105120000


class Task:
    def __init__(
        self,
        user_id: str,
        task_id: str,
        name: str,
        shortcut_flg: bool,
        children_task_id: list[str],
        done: bool,
        finished_workload: int,
        estimated_workload: int,
        deadline: datetime,
        notes: str,
    ):
        self._user_id = user_id
        self._task_id = task_id
        self._name = name
        self._shortcut_flg = shortcut_flg
        self._children_task_id = children_task_id
        self._done = done
        self._finished_workload = finished_workload
        self._estimated_workload = estimated_workload
        self._deadline = deadline
        self._notes = notes

    @classmethod
    def create_root(cls, user_id: str) -> Task:
        return cls(
            user_id=user_id,
            task_id=ROOT_TASK_ID,
            name=ROOT_TASK_NAME,
            shortcut_flg=True,
            children_task_id=[],
            done=False,
            finished_workload=ROOT_TASK_WORKLOAD,
            estimated_workload=ROOT_TASK_WORKLOAD,
            deadline="2200-12-31",
            notes="",
        )
