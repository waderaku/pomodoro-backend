from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    task_id: str


def update_task_service(
    user_id: str,
    task_id: str,
    name: str,
    estimated_workload: int,
    deadline: datetime,
    notes: str,
    done: bool,
):
    pass
