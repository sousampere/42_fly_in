
from abc import ABC, abstractmethod
from typing import Generator

from src.misc.is_state_solved import is_state_solved
from src.MapState import State


class AbstractStateProcessor(ABC):
    @abstractmethod
    def yield_process(self, state: State) -> Generator:
        """ Process each turn by yielding
        the current State progression """
        pass


class StateProcessor(AbstractStateProcessor):
    def yield_process(self, state: State) -> Generator:
        while not is_state_solved(state):
            for drone in state.drone_names:
                self.calculate_shortest_path(drone, state)
    
    @staticmethod
    def calculate_shortest_path(drone_name: str, state: State) -> str | None:
        # Search for the drone
        for zone in state.zones:
            if drone_name in [drone.name for drone in zone.drones]:
                # Drone found.

                # Return none if drone is at the end already
                if zone.is_end:
                    return None

                