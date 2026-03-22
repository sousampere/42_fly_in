
from pydantic import BaseModel, Field
from typing import List

from src.state_components.Zone import Zone
from src.state_components.Connection import Connection


class State(BaseModel):
    """State of the operation
    Class containing zones and their connections"""

    zones: List[Zone] = Field(default=[])
    connection: List[Connection] = Field(default=[])

    def __str__(self):
        zones = "\n".join(zone.__str__() for zone in self.zones)
        string = f"=== BEGIN STATE ===\n{zones}\n\n=== END STATE ==="

        return string