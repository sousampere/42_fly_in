from abc import ABC, abstractmethod
from sqlite3 import connect
from typing import Generator

from src.MapState.Connection import Connection
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
        # for zone in state.zones:

        # return available_zones
    
    @staticmethod
    def move_drone(state: State, drone_name: str, destination: Zone | Connection, going_to: Zone = None) -> State:
        # Check zones for the drone
        drone_found = False
        drone_copy = None
        for zone in state.zones:
            if drone_name in [drone.name for drone in zone.drones]:
                # Remove drone from current zone
                for drone in zone.drones:
                    if drone.name == drone_name:
                        drone_copy = drone
                        zone.drones.remove(drone)
                        drone_found = True
        
        # Check 
        for connection in state.connections:
            if drone_name in [d['drone'] for d in connection.drones]:
                # Remove drone
                for drone_data in connection.drones:
                    if drone_data['drone'].name == drone_name:
                        drone_copy = drone_data['drone']
                        connection.drones.remove(drone_data)
                        drone_found = True

        # Return current state if drone is not found
        if not drone_found:
            return state

        # Copy drone in zone
        if isinstance(destination, Zone):
            for zone in state.zones:
                if zone.name == destination.name:
                    zone.drones.append(drone_copy)
        
        # Copy drone in connection
        if isinstance(destination, Connection):
            for connection in state.connections:
                if connection.zones == destination.zones:
                    connection.drones.append(
                        {
                            'drone': drone_copy,
                            'going_to': going_to
                        }
                    )

        return state
