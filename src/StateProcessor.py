
from abc import ABC, abstractmethod
from typing import Generator

from src.MapState.Zone import Zone
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

                # Get avaiable zones
                zones_list: list[str] = StateProcessor.get_zone_connections(state, zone)

                # Select the zone with less cost
                for available_zone in sorted(zones_list, key=lambda z: z['cost']):
                    if available_zone['max_link_capacity'] < available_zone['current_nb_drones']:
                        pass

                print(f'{zone.name}___{zones_list}')
    
    @staticmethod
    def get_zone_connections(state: State, current_zone: Zone):
        """ Return a list of the available zones and their cost """
        available_zones = []
        for connection in state.connections:
            if current_zone.name in connection.zones:
                for name in connection.zones:
                    if name != current_zone.name:
                        available_zones.append(
                            {
                                'name': name,
                                'cost': connection.cost,
                                'max_link_capacity': connection.max_link_capacity,
                                'current_nb_drones': len(connection.drones)
                            }
                        )

        return available_zones
    
