
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import List, Dict, Any

from src.state_components.Drone import Drone


class ZoneConfigurationError(Exception):
    """Zone Configuration Error"""
    pass


class Color(Enum):
    """Enumeration of different colors possible"""
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    GRAY = "gray"
    BLUE = "blue"
    PURPLE = "purple"
    BLACK = "black"
    BROWN = "brown"
    ORANGE = "orange"
    MAROON = "maroon"
    GOLD = "gold"
    DARKRED = "darkred"
    VIOLET = "violet"
    CRIMSON = "crimson"
    RAINBOW = "rainbow"
    CYAN = "cyan"
    LIME = "lime"
    MAGENTA = "magenta"


class ZoneType(Enum):
    """Enumeration of different zone types possible"""
    RESTRICTED = "restricted"
    NORMAL = "normal"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Zone(BaseModel):
    """Zone object"""

    color: Color = Field(default=None)
    name: str
    x: int = Field()
    y: int = Field()
    type: ZoneType = Field(default=ZoneType.NORMAL)
    max_drones: int = Field(default=1, ge=0)
    drones: List[Drone] = Field(default=[])
    is_end_hub: bool = Field(default=False)
    connections: List[Dict[str, Any]] = []
    # Connection is a dict that contains :
    # 'zone': Zone,
    # 'max_link_capacity': int

    @model_validator(mode="after")
    def verify_data(self) -> "Zone":
        if "-" in self.name:
            raise ZoneConfigurationError(
                f"Invalid zone name {self.name}"
                ". A zone name can not contain "
                "dashes in its name."
            )
        return self

    def __str__(self):
        return (
            f"Zone {self.name} at X:{self.x} & Y:{self.y}, "
            f"type {self.type.value}, {self.max_drones} max drones "
            f"of color {self.color.value}. Contains "
            f"{', '.join((map(lambda drone: str(drone), self.drones)))}. "
            f"Connections: {list(map(lambda c: c['zone'].name, self.connections))} "
            f"end:{self.is_end_hub}"
        )

    def create_drones(self, number: int):
        drone_id = 1
        for _ in range(number):
            self.drones.append(Drone(name=f"D{drone_id}"))
            drone_id += 1
