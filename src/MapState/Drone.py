
from typing import Any

from pydantic import BaseModel, Field


class Drone(BaseModel):
    """ Object representing a Drone """
    name: str
    last_visited: list[Any] = Field(default=[])

    def __str__(self) -> str:
        """ String representation of the drone """
        return self.name
