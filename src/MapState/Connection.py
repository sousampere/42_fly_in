
from pydantic import BaseModel, Field

from src.MapState.Drone import Drone
from src.MapState.Zone import Zone


class Connection(BaseModel):
    zones: list[str] = []
    drones: list[dict[str, Drone | Zone]] = []
    # example: [
    #   {'drone': Drone, 'going_to': Zone}
    # ]
    max_link_capacity: int = Field(default=1)

    def __str__(self) -> str:
        return f'{self.zones[0]}<->{self.zones[1]} max:{self.max_link_capacity}'