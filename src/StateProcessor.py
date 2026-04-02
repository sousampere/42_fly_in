from abc import ABC, abstractmethod
import math
from typing import Any

from src.MapState.Connection import Connection
from src.MapState.Zone import Zone, ZoneType
from src.MapState.State import State


class AbstractStateProcessor(ABC):
    """Abstract class to create future state processors"""

    @abstractmethod
    def process(self, state: State) -> State:
        """Retunrs the next step"""
        pass


class StateProcessor(AbstractStateProcessor):
    """Class to process a state"""

    @staticmethod
    def process(state: State) -> State:
        if StateProcessor.is_completed(state):
            return state

        for drone_name in state.drone_names:
            # Get drone location
            drone_location = StateProcessor.get_drone_location(
                state, drone_name)
            if isinstance(drone_location, Connection):
                # Move drone if it is on a connection
                next_zone = drone_location.get_drone_next_zone(drone_name)
                state = StateProcessor.move_drone(
                    state, drone_name, next_zone, state.zones[0]
                )
            else:
                shortest_path = StateProcessor.get_shortest_path(
                    state, drone_name)
                if shortest_path is not None:
                    state = StateProcessor.move_drone(
                        state, drone_name, shortest_path, state.zones[0]
                    )

        # Reset moving counter for each connection
        for connection in state.connections:
            connection.moving = len(connection.drones)
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
                if drone["drone"].name == drone_name:
                    return [drone["going_to"]]

        # Drone found in Zone
        if isinstance(drone_origin, Zone):
            neighbours = StateProcessor.get_neighbour_zones(
                state, drone_origin)
            return neighbours

        return []

    @staticmethod
    def str_to_zone(state: State, zone_name: str) -> Zone | None:
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
        available_zones: list[Zone] = []
        # Check all connections
        for connection in state.connections:
            # Check if there is the zone in it
            # if current_zone.name in connection.zones and
            # connection.moving < connection.max_link_capacity:
            if current_zone.name in connection.zones:
                for name in connection.zones:
                    if name != current_zone.name:
                        new_neighbour = StateProcessor.str_to_zone(state, name)
                        if new_neighbour is None:
                            continue
                        if new_neighbour.zone_type != ZoneType.BLOCKED:
                            available_zones.append(new_neighbour)

        return available_zones

    @staticmethod
    def get_drone_location(state: State,
                           drone_name: str) -> Zone | Connection | None:
        """Return the zone object where a given drone is located"""
        for zone in state.zones:
            if drone_name in [d.name for d in zone.drones]:
                return zone

        for connection in state.connections:
            if drone_name in [d["drone"].name for d in connection.drones]:
                return connection

        return None

    @staticmethod
    def move_drone(
        state: State, drone_name: str,
        destination: Zone | Connection, going_to: Zone
    ) -> State:
        """Move a drone to a Zone or a Connection.

        Args:
            state (State): Current State
            drone_name (str): Name of the drone
            destination (Zone | Connection): Destination
            going_to (Zone, optional): Aimed zone if it is on a Connection.
            Defaults to None.

        Returns:
            State: New State
        """
        # Check zones for the drone
        if destination is None:
            return state

        current_location = StateProcessor.get_drone_location(state, drone_name)

        # Update Connection.moving
        if isinstance(destination, Zone):
            if isinstance(current_location, Zone):
                zone_connection = StateProcessor.get_zone_connection(
                    state, destination, current_location
                )
                for connection in state.connections:
                    if (
                        isinstance(zone_connection, Connection)
                        and connection.zones[0] == zone_connection.zones[0]
                        and connection.zones[1] == zone_connection.zones[1]
                    ):
                        connection.moving += 1

        if isinstance(destination, Zone):
            # If the zone is restricted and the drone is on a zone
            if destination.zone_type == ZoneType.RESTRICTED and isinstance(
                current_location, Zone
            ):
                # Update _future_drones count
                for zone in state.zones:
                    if zone.name == destination.name:
                        zone._future_drones += 1

                # Move to the connection instead
                for connection in state.connections:
                    if (
                        connection.zones[0] == destination.name
                        and connection.zones[1] == current_location.name
                        or connection.zones[1] == destination.name
                        and connection.zones[0] == current_location.name
                    ):
                        return StateProcessor.move_drone(
                            state, drone_name, connection, destination
                        )

        if (
            isinstance(destination, Zone)
            and destination.zone_type == ZoneType.RESTRICTED
            and isinstance(current_location, Connection)
        ):
            for zone in state.zones:
                if zone.name == destination.name:
                    zone._future_drones -= 1

        drone_found = False
        for zone in state.zones:
            if drone_name in [drone.name for drone in zone.drones]:
                # Remove drone from current zone
                for drone in zone.drones:
                    if drone.name == drone_name:
                        drone_copy = drone
                        drone_copy.last_visited.append(zone)
                        zone.drones.remove(drone)
                        drone_found = True

        # Remove drone from a connection
        for connection in state.connections:
            for drone_data in connection.drones:
                if drone_data["drone"].name == drone_name:
                    drone_copy = drone_data["drone"]
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
                        {"drone": drone_copy, "going_to": going_to}
                    )
                    connection.moving += 1

        return state

    @staticmethod
    def get_shortest_path(state: State,
                          drone_name: str) -> Zone | Connection | None:
        """Return the zone/connection of the next shortest path

        Args:
            state (State): Current state
            drone_name (str): name of the drone to get its position

        Returns:
            Zone | Connection | None: Next zone/connection
        """
        available_zones = StateProcessor.get_next_zones(state, drone_name)
        current_location = StateProcessor.get_drone_location(state, drone_name)

        for zone in available_zones:
            if zone.is_end:
                return zone

        # Ignore if drone on END zone
        if isinstance(current_location, Zone) and current_location.is_end:
            return None

        sort = sorted(
            available_zones,
            key=lambda z: StateProcessor.calculate_distance_from_end(state, z),
        )
        if len(sort) == 0:
            return None
        min_distance = StateProcessor.calculate_distance_from_end(
            state, sort[0])

        # Remove unusable paths to zones
        for zone in sort:
            if not StateProcessor.check_capacity_allowance(
                state, current_location, zone
            ):
                sort.remove(zone)

        for zone in sort:
            if (
                zone in StateProcessor.get_drone_last_visided_zone(
                    state, drone_name)
                or zone.zone_type == ZoneType.BLOCKED
            ):
                sort.remove(zone)

        # Prevent going to zones where there will not be enough spaces
        for zone in sort:
            if (
                len(zone.drones) + zone._future_drones == zone.max_drones
                and not zone.is_end
            ):
                sort.remove(zone)

        if len(sort) == 0:
            return None

        # Return a priority zone if its
        # distance is = to the minimum
        # min_distance = StateProcessor.
        # calculate_distance_from_end(state, sort[0])
        for zone in sort:
            if isinstance(zone, Zone):
                # if StateProcessor.calculate_distan
                # ce_from_end(state, zone) == min_distance:
                if (
                    StateProcessor.calculate_distance_from_end(state, zone)
                    == min_distance
                ):
                    if zone.zone_type == ZoneType.PRIORITY:
                        return zone
                else:
                    break

        print(f"---- Drone {drone_name} has best route at {sort[0]}")

        if StateProcessor.calculate_distance_from_end(
           state, sort[0]) > min_distance:
            return None

        # print(f'Shortest path for {drone_name}: {sort[0]}')
        return sort[0]

    @staticmethod
    def calculate_distance_from_end(
        state: State, start_zone: Zone
    ) -> int | float | Any:
        """Djikstra algorithm to find the distance of
        a zone to the end (in turn costs)

        Args:
            state (State): current state
            start_zone (Zone): zone to calculate distance

        Returns:
            int | float | Any: distance
        """
        # Queue containing the zones
        queue: list[Any] = []

        # Add the current zone and a base cost of zero to each zone
        queue.append([0, start_zone])

        # Dictionary to track the minimum cost found to reach each zone
        min_costs = {start_zone.name: 0}

        # While there are elements in the queue
        while queue:

            # ---- Block of code to get the zone with the minimum cost ----
            min_index = 0
            # For each zone, check its cost
            for i in range(1, len(queue)):
                if queue[i][0] < queue[min_index][0]:
                    # If the cost is less, save its position
                    min_index = i

            # Then extract the zone with the lowest cost
            current_cost, current_zone = queue.pop(min_index)

            # Return the current cost if the zone is the end
            # (final case of the loop)
            if current_zone.is_end:
                return current_cost

            # Gets neighbors zones
            neighbors = StateProcessor.get_neighbour_zones(state, current_zone)

            for neighbor in neighbors:
                # Ignore blocked zones
                if neighbor.zone_type != ZoneType.BLOCKED:
                    # Calculate cost
                    new_cost = current_cost + StateProcessor.get_cost(
                        state, current_zone, neighbor
                    )

                    # If we found a shorter path to this neighbor
                    if new_cost < min_costs.get(neighbor.name, math.inf):
                        min_costs[neighbor.name] = new_cost

                        # Add to list
                        queue.append([new_cost, neighbor])

        return math.inf  # End never reached

    @staticmethod
    def get_cost(state: State, zone_1: Zone, zone_2: Zone) -> int:
        for connection in state.connections:
            if zone_1.name in connection.zones:
                if zone_2.name in connection.zones:
                    return connection.cost
            if zone_2.name in connection.zones:
                if zone_1.name in connection.zones:
                    return connection.cost
        return 0

    @staticmethod
    def get_drone_last_visided_zone(state: State,
                                    drone_name: str) -> list[Any]:
        for zone in state.zones:
            for drone in zone.drones:
                if drone_name == drone.name:
                    return drone.last_visited
        return []

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
            if isinstance(location, Connection):
                return False
            if location is not None and location.is_end is not True:
                return False
        return True

    @staticmethod
    def get_zone_connection(
        state: State, zone_1: Zone, zone_2: Zone
    ) -> Connection | None:
        for connection in state.connections:
            if (
                connection.zones[0] == zone_1.name
                and connection.zones[1] == zone_2.name
                or connection.zones[0] == zone_2.name
                and connection.zones[1] == zone_1.name
            ):
                return connection
        return connection

    @staticmethod
    def check_capacity_allowance(state: State,
                                 location: Any,
                                 destination: Any) -> bool:
        connection = StateProcessor.get_zone_connection(state,
                                                        location,
                                                        destination)

        # Connection not found
        if connection is None:
            return True

        # Connection.
        if destination.is_end:
            return True

        # Don't exceed the max_drone_capacity
        if (
            destination.max_drones
            == len(destination.drones) + destination._future_drones
        ):
            return False

        if connection.moving >= connection.max_link_capacity:
            return False

        return True
