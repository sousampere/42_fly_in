
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, model_validator

from src.MapState.Drone import Drone


class ZoneError(Exception):
    """ Zone exception class """
    pass


class ZoneNameError(ZoneError):
    """ Zone name exception class """
    pass


class ZoneType(Enum):
    """ Enumeration of zone types """
    NORMAL = 'normal'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
    BLOCKED = 'blocked'


class Zone(BaseModel):
    """ Representation of a zone as an object """
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
        """ Validate data, raise an error if invalid """
        if '-' in self.name:
            raise ZoneNameError('Zone name can\'t have a "-" character.')
        return self

    def __str__(self) -> str:
        return f'{self.name}'

    def __hash__(self) -> int:
        return hash(self.name + ''.join(
            [d.name for d in self.drones]) + str(self._future_drones))
