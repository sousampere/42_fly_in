from abc import ABC, abstractmethod
import random
from typing import Generator

from src.MapState.Connection import Connection
from src.MapState.Drone import Drone
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
    def process(state: State) -> State:
        for drone_name in state.drone_names:
            shortest_path = StateProcessor.get_shortest_path(state, drone_name)
            state = StateProcessor.move_drone(state, drone_name, shortest_path)
        return state

    @staticmethod
    def get_next_zones(state: State, drone_name: str) -> list[Zone]:
        """Get a list for the name of the available zones of a given drone

        Args:
            state (State): Current state
            drone_name (str): drone_id

        Returns:
            list[Zone]: list of zones, sorted by best
        """
        drone_origin = StateProcessor.get_drone_location(state, drone_name)

        # Drone not found
        if drone_origin is None:
            return []

        # Drone found in connection
        if isinstance(drone_origin, Connection):
            for drone in drone_origin.drones:
                if drone['drone'].name == drone_name:
                    return [drone['going_to']]

        # Drone found in Zone
        if isinstance(drone_origin, Zone):
            return StateProcessor.get_neighbour_zones(state, drone_origin)
    
    @staticmethod
    def str_to_zone(state: State, zone_name: str) -> Zone:
        """Give it a zone name (str), and it will give back
        the corresponding Zone object

        Args:
            state (State): Current state
            zone_name (str): Name of the zone

        Returns:
            Zone: Corresponding Zone
        """
        for zone in state.zones:
            if zone.name == zone_name:
                return zone
        return None

    @staticmethod
    def get_neighbour_zones(state: State, current_zone: Zone) -> list[Zone]:
        available_zones = []
        # Check all connections
        for connection in state.connections:
            # Check if there is the zone in it
            if current_zone.name in connection.zones:
                for name in connection.zones:
                    if name != current_zone.name:
                        available_zones.append(StateProcessor.str_to_zone(state, name))

        return available_zones


    @staticmethod
    def get_drone_location(state: State, drone_name: str) -> Zone | Connection | None:
        """ Return the zone object where a given drone is located """
        for zone in state.zones:
            if drone_name in [d.name for d in zone.drones]:
                return zone
        
        for connection in state.connections:
            if drone_name in [d['drone'].name for d in connection.drones]:
                return connection

        return None
    
    @staticmethod
    def move_drone(state: State, drone_name: str, destination: Zone | Connection, going_to: Zone = None) -> State:
        """Move a drone to a Zone or a Connection.

        Args:
            state (State): Current State
            drone_name (str): Name of the drone
            destination (Zone | Connection): Destination
            going_to (Zone, optional): Aimed zone if it is on a Connection. Defaults to None.

        Returns:
            State: New State
        """
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

    @staticmethod
    def get_shortest_path(state: State, drone_name: str) -> Zone | Connection:
        available_zones = StateProcessor.get_next_zones(state, drone_name)
        return random.choice(available_zones)

    @staticmethod
    def calculate_distance_from_end(state: State, zone: Zone, visited: set[Zone] = set(), cost: int = 0) -> int:
        if zone.is_end:
            return cost

        # List of neighbour zones
        neighbours = []
        for neighbour in StateProcessor.get_neighbour_zones(state, zone):
            if neighbour.name not in visited:
                n_cost = StateProcessor.calculate_distance_from_end(state, neighbour, visited.union({neighbour.name}), cost + 1)
                if n_cost is not None:
                    neighbours.append({
                        'name': neighbour.name,
                        'cost': n_cost
                    })