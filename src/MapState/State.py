

from pydantic import BaseModel

from src.MapState.Connection import Connection
from src.MapState.Zone import Zone


class State:
    """ State that contains the available """
    def __init__(self, zones: list[Zone] = [], connections: list[Connection] = []):
        self.zones = zones
        self.connections = connections
    
    def __str__(self) -> str:
        return f'Containing {len(self.zones)} zones and {len(self.connections)} connections.'