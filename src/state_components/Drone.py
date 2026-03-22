
from pydantic import BaseModel


class Drone(BaseModel):
    """Drone object"""

    name: str

    def __str__(self):
        return self.name
