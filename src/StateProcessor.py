from abc import ABC, abstractmethod
from typing import Generator

from src.MapState.Zone import Zone
from src.misc.is_state_solved import is_state_solved
from src.MapState.State import State


class AbstractStateProcessor(ABC):
    @abstractmethod
    def yield_process(self, state: State) -> Generator:
        """Process each turn by yielding
        the current State progression"""
        pass


class StateProcessor(AbstractStateProcessor):
    def yield_process(self, state: State) -> Generator:
        while not is_state_solved(state):
            for drone in state.drone_names:
                self.calculate_shortest_path(drone, state)

    @staticmethod
    def process_connections(state: State) -> State:
        pass

    @staticmethod
    def calculate_shortest_path(state: State, drone_name: str):
        for zone in state.zones:
            if drone_name in [d.name for d in zone.drones]:
                # Drone found, continuig
                pass

    @staticmethod
    def get_next_zones(state: State, drone_name: str):
        """Returns a list of choices sorted by the best choice"""
        # Search all zones for the drone
        available_zones = []
        for zone in state.zones:
            if drone_name in [d.name for d in zone.drones]:
                # Drone found in zone
                # Checking all connected zones
                for connection in state.connections:
                    if zone.name in connection.zones:
                        # Current connection has the zone
                        for conn_zone in connection.zones:
                            if conn_zone != zone.name:  # Get the distant zone name
                                for state_zone in state.zones:
                                    # Add the zone to the list if it has space
                                    if (
                                        state_zone.name == zone.name
                                        and len(state_zone.drones)
                                        < state_zone.max_drones
                                    ):
                                        available_zones.append(state_zone)

        # If zones found, return, else -> search in the connections
        if len(available_zones) != 0:
            return available_zones

        for connection in state.connections:
            for drone in connection.drones:
                if drone["drone"].name == drone_name:
                    available_zones.append(drone["going_to"])
        return available_zones
