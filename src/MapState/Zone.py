
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, model_validator

from src.MapState.Drone import Drone


class ZoneError(Exception):
    pass

class ZoneNameError(ZoneError):
    pass


class ZoneType(Enum):
    NORMAL = 'normal'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
    BLOCKED = 'blocked'


class Zone(BaseModel):
    name: str
    x: int
    y: int
    is_start: bool = False
    is_end: bool = False
    color: str = Field(default='white')
    max_drones: int = Field(ge=0, default=1)
    zone_type: ZoneType = Field(default=ZoneType.NORMAL)
    drones: List[Drone] = []
    _future_drones: int = 0

    @model_validator(mode='after')
    def verify(self) -> "Zone":
        if '-' in self.name:
            raise ZoneNameError('Zone name can\'t have a "-" character.')
        return self

    def __str__(self) -> str:
        return f'Zone "{self.name}" at ({self.x}, {self.y}), | '\
        f'Color={self.color}, Max_drones={self.max_drones}, '\
        f'of type {self.zone_type.value}'
    
    def __hash__(self):
        return hash(self.name)