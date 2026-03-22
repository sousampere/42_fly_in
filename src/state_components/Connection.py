
from typing import List
from pydantic import BaseModel

from src.state_components.Zone import Zone


class Connection(BaseModel):
    zones: List[Zone] = []
    max_drone_capacity: int = 1
