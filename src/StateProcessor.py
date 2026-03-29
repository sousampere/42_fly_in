from abc import ABC, abstractmethod
from functools import lru_cache
import math
import random
from typing import Any, Generator

from src.MapState.Connection import Connection
from src.MapState.Drone import Drone
from src.MapState.Zone import Zone, ZoneType
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
        if StateProcessor.is_completed(state):
            return state

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
            neighbours = StateProcessor.get_neighbour_zones(state, drone_origin)
            return neighbours
    
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
                        new_neighbour = StateProcessor.str_to_zone(state, name)
                        if new_neighbour.zone_type != ZoneType.BLOCKED:
                            available_zones.append(new_neighbour)

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
        if destination is None:
            return state
        drone_found = False
        drone_copy = None
        for zone in state.zones:
            if drone_name in [drone.name for drone in zone.drones]:
                # Remove drone from current zone
                for drone in zone.drones:
                    if drone.name == drone_name:
                        drone_copy = drone
                        drone_copy.last_visited.append(zone)
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
        sort = sorted(available_zones, key=lambda z: StateProcessor.calculate_distance_from_end(state, z))
        if len(sort) == 0:
            return None

        # Return a priority zone if its distance is = to the minimum
        min_distance = StateProcessor.calculate_distance_from_end(state, sort[0])
        for zone in sort:
            if isinstance(zone, Zone):
                if StateProcessor.calculate_distance_from_end(state, zone) == min_distance:
                    if zone.zone_type == ZoneType.PRIORITY:
                        return zone
                else:
                    break

        for zone in sort:
            if zone in StateProcessor.get_drone_last_visided_zone(state, drone_name) \
                or zone.zone_type == ZoneType.BLOCKED:
                sort.remove(zone)

        return sort[0]

    @staticmethod
    def calculate_distance_from_end(state: State, zone: Zone, visited: set[Zone] = None, cost: int = 0) -> int:
        if visited is None:
            visited = set()

        # Final case
        if zone.is_end:
            return cost

        # Mark current zone as visited
        visited.add(zone.name)

        neighbors = StateProcessor.get_neighbour_zones(state, zone)
        distances = []

        for neighbor in neighbors:
            if neighbor.name not in visited and neighbor.zone_type != ZoneType.BLOCKED:
                distances.append(StateProcessor.calculate_distance_from_end(state, neighbor, visited.copy(), cost + 1))

        return (min(distances) if distances else math.inf)

    @staticmethod
    def get_drone_last_visided_zone(state: State, drone_name: str) -> list[Any] | None:
        for zone in state.zones:
            for drone in zone.drones:
                if drone_name == drone.name:
                    return drone.last_visited
        return None

    @staticmethod
    def is_completed(state: State) -> bool:
        """Return true if the state is completed

        Args:
            state (State): Current State

        Returns:
            bool: is completed ?
        """
        for drone in state.drone_names:
            location = StateProcessor.get_drone_location(state, drone)
            if location is not None and location.is_end is not True:
                return False
        return True