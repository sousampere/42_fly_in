

from pydantic import BaseModel

from src.MapState.Connection import Connection
from src.MapState.Zone import Zone


class State:
    """ State that contains the available """
    def __init__(self, zones: list[Zone] = [], connections: list[Connection] = []):
        self.zones: list[Zone] = zones
        self.connections: list[Connection] = connections
        self.drone_names: list[str] = []

        # Get all drone names
        for zone in zones:
            for drone in zone.drones:
                self.drone_names.append(drone.name)
        
        return None

    
    def __str__(self) -> str:
        return f'Containing {len(self.zones)} zones and {len(self.connections)} connections.'