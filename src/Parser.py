
from abc import ABC, abstractmethod
from typing import List

from src.state_components.Connection import Connection
from src.state_components.State import State
from src.state_components.Zone import Zone, ZoneType


class ConfigException(Exception):
    pass


class AbstractParser(ABC):
    @abstractmethod
    def parse(file_path: str) -> State:
        pass


class Parser(AbstractParser):
    @staticmethod
    def parse(file_path: str) -> State:
        with open(file_path, 'r') as f:
            file_content = f.readlines()
        
        # Ignore comments
        file_content = Parser.ignore_comments(file_content)

        # Get number of drones
        nb_drones = Parser.get_nb_drones(file_content)

        # Get zones
        zones = Parser.get_zones(file_content)
        
        return State(
            zones=zones)

    @staticmethod
    def ignore_comments(lines: List[str]) -> List[str]:
        content = []
        for line in lines:
            content.append(line.split('#')[0])
        return content

    @staticmethod
    def get_nb_drones(lines: List[str]) -> int:
        for line in lines:
            if line.startswith('nb_drones:'):
                split = line.split(':')[1].strip()
                try:
                    return int(split)
                except ValueError:
                    raise ConfigException('Invalid number of '
                                          'drones provided.')

    @staticmethod
    def get_zones(lines: List[str]) -> List[Zone]:
        zones = []

        for line in lines:
            if line.startswith(('hub:', 'end_hub', 'start_hub')):
                split = line.split('[')
                zone_base_data = split[0].split(' ')
                name = zone_base_data[1]
                x = zone_base_data[2]
                y = zone_base_data[3]
                color = None
                max_drones = 1
                zone_type = ZoneType.NORMAL

                # Getting attributes
                attributes = split[1].strip('[]')
                for attrib in attributes.split(' '):
                    attrib = attrib.split('=')
                    if len(attrib) != 2:
                        raise ConfigException('Invalid config '
                                              f'line: "{line}"')
                    attrib[1] = attrib[1].strip('\n[]')
                    if attrib[0] == 'color':
                        color = attrib[1]
                    if attrib[0] == 'max_drones':
                        try:
                            max_drones = int(attrib[1])
                        except ValueError:
                            raise ConfigException('Invalid max_drone '
                                                  f'at line "{line}"')
                    if attrib[0] == 'zone':
                        zone_type = attrib[1]
                zones.append(Zone(
                    name=name,
                    x=x,
                    y=y,
                    color=color,
                    zone_type=zone_type,
                    max_drones=max_drones,
                    is_end_hub=True if zone_base_data[0] == 'end_hub:'
                    else False
                ))
        return zones
    
    @staticmethod
    def get_connections(lines: List[str]) -> List[Connection]:
        for line in lines:
            if line.startswith('connection:'):
                line = line.split(' ')
                if len(line) != 2:
                    raise ConfigException('Invalid config '
                                            f'line: "{line}"')
                if 