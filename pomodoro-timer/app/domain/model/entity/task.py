from __future__ import annotations

from datetime import datetime


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
    def create_root(cls, user_id: str):
        return cls(
            user_id=user_id,
            task_id="root",
            name="全ての親タスク",
            shortcut_flg=False,
            children_task_id=[],
            done=False,
            finished_workload=0,
            estimated_workload=0,
            deadline="",
            notes="",
        )
