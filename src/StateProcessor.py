from abc import ABC, abstractmethod
import math
from re import L
from typing import Any, Generator
from collections import deque

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
            # Get drone location
            drone_location = StateProcessor.get_drone_location(state, drone_name)
            if isinstance(drone_location, Connection):
                # Move drone if it is on a connection
                next_zone = drone_location.get_drone_next_zone(drone_name)
                state = StateProcessor.move_drone(state, drone_name, next_zone)
            else:
                shortest_path = StateProcessor.get_shortest_path(state, drone_name)
                state = StateProcessor.move_drone(state, drone_name, shortest_path)
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
        print('Moving drone to ', destination)
        # Check zones for the drone
        if destination is None:
            print('Destination is NONE !')
            return state
        
        current_location = StateProcessor.get_drone_location(state, drone_name)
        # Update Connection.moving
        if isinstance(destination, Zone):
            if isinstance(current_location, Zone):
                zone_connection = StateProcessor.get_zone_connection(state, destination, current_location)
                for connection in state.connections:
                    if connection.zones[0] == zone_connection.zones[0] and connection.zones[1] == zone_connection.zones[1]:
                        connection.moving += 1
        
        if isinstance(destination, Zone):
            # If the zone is restricted and the drone is on a zone
            if destination.zone_type == ZoneType.RESTRICTED \
                and isinstance(current_location, Zone):
                # Move to a connection instead
                for connection in state.connections:
                    if connection.zones[0] == destination.name and connection.zones[1] == current_location.name \
                    or connection.zones[1] == destination.name and connection.zones[0] == current_location.name:
                        return StateProcessor.move_drone(state, drone_name, connection, destination)
                # Update _future_drones count
                for zone in state.zones:
                    if zone.name == destination.name:
                        zone._future_drones += 1

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

        # Remove drone from a connection
        for connection in state.connections:
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
        current_location = StateProcessor.get_drone_location(state, drone_name)

        # Ignore if drone on END zone
        if isinstance(current_location, Zone) and current_location.is_end:
            return None

        sort = sorted(available_zones, key=lambda z: StateProcessor.test(state, z))
        if len(sort) == 0:
            return None

        # Return a priority zone if its distance is = to the minimum
        # min_distance = StateProcessor.calculate_distance_from_end(state, sort[0])
        min_distance = StateProcessor.test(state, sort[0])
        for zone in sort:
            if isinstance(zone, Zone):
                # if StateProcessor.calculate_distance_from_end(state, zone) == min_distance:
                if StateProcessor.test(state, zone) == min_distance:
                    if zone.zone_type == ZoneType.PRIORITY:
                        return zone
                else:
                    break


        for zone in sort:
            if zone in StateProcessor.get_drone_last_visided_zone(state, drone_name) \
                or zone.zone_type == ZoneType.BLOCKED:
                sort.remove(zone)
        
        # Remove unusable paths to zones
        for zone in sort:
            if not StateProcessor.check_capacity_allowance(state, current_location, zone):
                sort.remove(zone)

        if len(sort) == 0:
            return None

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
                if neighbor.zone_type == ZoneType.RESTRICTED:
                    distances.append(StateProcessor.calculate_distance_from_end(state, neighbor, visited.copy(), cost + 2))
                else:
                    distances.append(StateProcessor.calculate_distance_from_end(state, neighbor, visited.copy(), cost + 1))

        return (min(distances) if distances else math.inf)
    



    @staticmethod
    def test(state: State, start_zone: Zone) -> int | float:
        import math
        import heapq
        import itertools
        # Utilisation d'une file de priorité (min-heap) pour l'algorithme de Dijkstra
        queue = []

        # Compteur pour départager les zones avec le même coût dans la file de priorité
        # Cela évite une erreur si Python essaie de comparer deux objets Zone
        counter = itertools.count() 

        # La file contient des tuples : (coût_cumulé, compteur, zone_actuelle)
        heapq.heappush(queue, (0, next(counter), start_zone))

        # On remplace le set par un dictionnaire pour mémoriser le coût minimum pour atteindre chaque zone
        (start_zone.name)
        min_costs = {start_zone.name: 0}

        while queue:
            # On récupère toujours la zone accessible avec le plus petit coût cumulé
            current_cost, _, current_zone = heapq.heappop(queue)

            # Final case : comme on explore toujours le moins cher en premier, 
            # si on atteint la fin, c'est garanti d'être le chemin le plus court
            if current_zone.is_end:
                return current_cost

            # Optimisation : si on a extrait un chemin obsolète (un meilleur chemin
            # a été trouvé vers cette zone et ajouté à la file), on l'ignore
            if current_cost > min_costs.get(current_zone.name, math.inf):
                continue

            # On récupère les voisins
            neighbors = StateProcessor.get_neighbour_zones(state, current_zone)

            for neighbor in neighbors:
                if neighbor.zone_type != ZoneType.BLOCKED:
                    
                    # Le nouveau coût est le coût actuel + le coût pour entrer dans le voisin
                    new_cost = current_cost + StateProcessor.get_cost(state, current_zone, neighbor)
                    
                    # Si c'est la première fois qu'on voit ce voisin OU si on a trouvé un chemin moins cher
                    if new_cost < min_costs.get(neighbor.name, math.inf):
                        min_costs[neighbor.name] = new_cost
                        
                        # On ajoute le voisin à la file avec son nouveau coût cumulé
                        heapq.heappush(queue, (new_cost, next(counter), neighbor))

        # Si la file se vide sans trouver la fin, c'est un cul-de-sac
        return math.inf

    @staticmethod
    def get_cost(state: State, zone_1: Zone, zone_2: Zone) -> int:
        for connection in state.connections:
            if zone_1.name in connection.zones:
                if zone_2.name in connection.zones:
                    return connection.cost
            if zone_2.name in connection.zones:
                if zone_1.name in connection.zones:
                    return connection.cost
        return None

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
            if isinstance(location, Connection):
                return False
            if location is not None and location.is_end is not True:
                return False
        return True

    @staticmethod
    def get_zone_connection(state: State, zone_1: Zone, zone_2: Zone):
        for connection in state.connections:
            if connection.zones[0] == zone_1.name and connection.zones[1] == zone_2.name \
            or connection.zones[0] == zone_2.name and connection.zones[1] == zone_1.name:
                return connection
        return None

    @staticmethod
    def check_capacity_allowance(state: State, location: Zone, destination: Zone) -> bool:
        connection = StateProcessor.get_zone_connection(state, location, destination)

        # Connection not found
        if connection is None:
            return True

        # Connection.
        if destination.is_end:
            return True

        if destination.max_drones == len(destination.drones) + destination._future_drones \
            or connection.moving == connection.max_link_capacity:
            print(connection.moving, connection.max_link_capacity)
            return False

        return True
