#!/usr/bin/python3

from pydantic import BaseModel, model_validator, Field
from enum import Enum


class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    YELLOW = 'yellow'
    CYAN = 'cyan'
    MAGENTA = 'magenta'
    PURPLE = 'purple'
    ORANGE = 'orange'
    BLACK = 'black'
    WHITE = 'white'
    BROWN = 'brown'
    LIME = 'lime'
    GOLD = 'gold'
    DEFAULT = None


class HubType(Enum):
    START_HUB = 'start_hub'
    HUB = 'hub'
    END_HUB = 'end_hub'


class ZoneRestriction(Enum):
    RESTRICTED = 'restricted'
    NORMAL = 'normal'
    PRIORITY = 'priority'
    BLOCKED = 'blocked'
    


class Hub(BaseModel):
    type: HubType = Field(default=HubType.HUB)
    name: str = Field(json_schema_extra=r'^[^-]*$', default="zone", description="Name of the zone")
    x: int = Field(default=0)
    y: int = Field(default=0)
    color: Color = Field(default=Color.DEFAULT)
    max_drone: int | None = Field(default=None)
    restriction: ZoneRestriction = Field(default=ZoneRestriction.NORMAL)

    @model_validator(mode='after')
    def validate(self) -> "Hub":
        if '-' in self.name:
            raise ValueError('Zone name contains a \'-\' character.')
        if self.max_drone is not None and self.max_drone < 1:
            raise ValueError('Invalid max drones, must be >= 1.')
        if self.restriction == ZoneRestriction.BLOCKED and (self.type == HubType.END_HUB or self.type == HubType.START_HUB):
            raise ValueError('Start/End hub cannot be blocked.')
        return self

    def print_data(self):
        print(f'Name: {self.name}\n' +
            f'X|Y: {self.x}|{self.y}\n' +
            f'Type: {self.type._value_}\n' +
            f'Color: {self.color.value}\n' +
            f'Max_drone: {self.max_drone}\n' +
            f'Restriction: {self.restriction._value_}')
    

if __name__ == '__main__':
    zone = Hub(type='start_hub', name='start', x=0, y=0)
    zone.print_data()