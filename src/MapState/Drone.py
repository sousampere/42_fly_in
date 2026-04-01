
from typing import Any

from pydantic import BaseModel, Field


class Drone(BaseModel):
    name: str
    last_visited: list[Any] = Field(default=[])

    def __str__(self) -> str:
        return self.name
