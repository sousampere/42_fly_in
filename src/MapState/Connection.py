
from pydantic import BaseModel, Field

from MapState.Drone import Drone
from MapState.Zone import Zone


class Connection(BaseModel):
    zones: list[Zone] = []
    drones: list[Drone] = []
    max_link_capacity: int = Field(default=1)