from __future__ import annotations

from dataclasses import dataclass


@dataclass(init=True, eq=True, frozen=True)
class DefaultLength:
    work: int
    rest: int
