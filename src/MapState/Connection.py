
from typing import Any

from pydantic import BaseModel, Field

# from src.MapState.Drone import Drone


class Connection(BaseModel):
    """ Connection object """
    zones: list[str] = []
    drones: list[Any] = []
    # example: [
    #   {'drone': Drone, 'going_to': Zone}
    # ]
    max_link_capacity: int = Field(default=1)
    cost: int = Field(default=1)
    moving: int = Field(default=0)

    def __str__(self) -> str:
        """ String representation of the drone """
        return f'{self.zones[0]}<->{self.zones[1]} '\
               f'max:{self.max_link_capacity}, '\
               f'{'/'.join(d['drone'].name for d in self.drones)}'

    def get_drone_next_zone(self, drone_name: str) -> Any:
        """ Getter for the next drone  """
        for drone in self.drones:
            if drone['drone'].name == drone_name:
                return drone['going_to']

        return None
