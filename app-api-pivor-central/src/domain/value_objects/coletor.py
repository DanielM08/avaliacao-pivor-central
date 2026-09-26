from dataclasses import dataclass


@dataclass(frozen=True)
class Coletor:
    si: int
    dist: float | None = None
    v1: float | None = None
    v2: float | None = None
    v3: float | None = None
    v4: float | None = None
