

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
    
    def get_min_max_coords(self):
        # Get max and min coords
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        for zone in self.zones:
            x_min = min(zone.x, x_min)
            x_max = max(zone.x, x_max)
            y_min = min(zone.y, y_min)
            y_max = max(zone.y, y_max)
        
        return (x_min, x_max, y_min, y_max)

