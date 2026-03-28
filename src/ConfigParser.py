

from typing import List

from src.MapState.State import State
from src.MapState.Connection import Connection
from src.MapState.Drone import Drone
from src.MapState.Zone import Zone, ZoneError, ZoneType


class ConfigError(Exception):
    pass


class ConfigParser:
    @staticmethod
    def parse(file_path: str) -> State:
        with open(file_path, 'r') as f:
            commented_lines = f.readlines()

        # Remove comments
        lines = []
        for line in commented_lines:
            lines.append(line.split('#')[0])

        # Get drones
        drones = ConfigParser.get_drones(lines)

        # Get drones
        zones: List[Zone] = ConfigParser.get_zones(lines)

        # Add drones to the start_hub
        for zone in zones:
            if zone.is_start:
                zone.drones = drones

        # Create connections
        connections = ConfigParser.get_connections(lines=lines)

        # Create state
        state = State(zones=zones, connections=connections)

        return state

    def get_drones(lines: List[str]) -> List[Drone]:
        for index, line in enumerate(lines, start=1):
            if line.startswith('nb_drones:'):
                if len(line.split(' ')) != 2:
                    raise ConfigError(f'Invalid nb_drones at line {index}')
                try:
                    nb_drones = int(line.split(' ')[1])
                except Exception:
                    raise ConfigError(f'Invalid nb_drones at line {index}')
                if nb_drones <= 0:
                    raise ConfigError(f'Invalid nb_drones at line {index}. '
                                      'Must be >= 1.')

                # Creating drones
                drones = []
                drone_id = 1
                for _ in range(nb_drones):
                    drones.append(Drone(name=f'D{drone_id}'))
                    drone_id += 1
                return drones

        # No drone line found
        raise ConfigError('Could not find a number of drones in your config')

    def get_zones(lines: List[str]) -> List[Zone]:
        """ Returns the parsed result of the list of zones """
        zones = []
        for index, line in enumerate(lines, start=1):
            if line.startswith(('start_hub:', 'hub:', 'end_hub:')):
                if len(line.split('[')[0].strip().split(' ')) != 4:
                    raise ConfigError(f'Invalid zone at line {index}')
                name = line.split('[')[0].strip().split(' ')[1]
                x = line.split('[')[0].strip().split(' ')[2]
                y = line.split('[')[0].strip().split(' ')[3]
                is_end = True if line.startswith('end_hub:') else False
                is_start = True if line.startswith('start_hub:') else False
                zone_type = ZoneType.NORMAL
                color = 'white'
                max_drones = 1

                metadatas = line.split('[')[1].strip('[]').split(' ')
                for metadata in metadatas:
                    if len(metadata.split('=')) != 2:
                        raise ConfigError(f'Invalid metadata at line {index}')
                    match metadata.split('=')[0]:
                        case 'color':
                            color = metadata.split('=')[1].strip('\n]')
                        case 'zone':
                            zone_type = metadata.split('=')[1].strip('\n]')
                        case 'max_drones':
                            max_drones = metadata.split('=')[1].strip('\n]')

                try:
                    if name in [z.name for z in zones]:
                        raise ConfigError(f'Zone name already used at line {index}')
                    zones.append(Zone(name=name, x=x, y=y, is_end=is_end,
                                      color=color, max_drones=max_drones,
                                      zone_type=zone_type, is_start=is_start))
                except ZoneError as e:
                    raise ConfigError(f'Invalid zone at line {index}: {e}')

        return zones
    
    def get_connections(lines: list[str]) -> list[Connection]:
        connections = []
        for index, line in enumerate(lines, start=1):
            if line.startswith('connection:'):
                if len(line.split('[')[0].strip().split(' ')) != 2:
                    raise ConfigError(f'Invalid connection at line {index}')
                connection = line.split('[')[0].strip().split(' ')[1].split('-')
                if len(connection) != 2:
                    raise ConfigError(f'Invalid connection at line {index}')
                if connection[0] == connection[1]:
                    raise ConfigError(f'Invalid connection at line {index}')
                max_link_capacity = 1
                if len(line.split('[')) == 2:
                    if line.split('[')[1].strip('\n[]').split('=')[0] == 'max_link_capacity':
                        try:
                            max_link_capacity = int(line.split('[')[1].strip('\n[]').split('=')[1])
                        except Exception:
                            raise ConfigError(f'Invalid max_link_capacity at line {line}')
                connect = Connection(zones=[connection[0], connection[1]], max_link_capacity=max_link_capacity)
                connections.append(connect)
        return connections