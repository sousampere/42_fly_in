
from pydantic import BaseModel


class Drone(BaseModel):
    name: str

    def __str__(self) -> str:
        return self.name