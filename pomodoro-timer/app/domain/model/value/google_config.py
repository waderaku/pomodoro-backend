from __future__ import annotations

from dataclasses import dataclass


@dataclass(init=True, eq=True, frozen=True)
class Calendar:
    id: str
    name: str


@dataclass(init=True, eq=True, frozen=True)
class TaskList:
    id: str
    name: str


@dataclass(init=True, eq=True, frozen=True)
class GoogleConfig:
    calendar: Calendar
    task_list: TaskList
