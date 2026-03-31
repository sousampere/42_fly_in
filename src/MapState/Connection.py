
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
    cost: int = Field(default=1)
    moving: int = Field(default=0)

    def __str__(self) -> str:
        return f'{self.zones[0]}<->{self.zones[1]} max:{self.max_link_capacity}, {'/'.join(d['drone'].name for d in self.drones)}'

    def get_drone_next_zone(self, drone_name: str) -> Zone:
        for drone in self.drones:
            if drone['drone'].name == drone_name:
                return drone['going_to']
        return None