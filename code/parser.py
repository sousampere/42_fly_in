#!/usr/bin/python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parser.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/11 13:52:30 by gtourdia        #+#    #+#               #
#  Updated: 2026/02/21 15:25:02 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from objects.Hub import HubType, Hub, Color, ZoneRestriction

class ParserError(Exception):
    """ Exception specialized to parsing """
    pass

def get_nb_drones(line: str, current_line) -> int:
    """ Given a line from the configuration file, returns the number of drones """
    try:
        nb_drones = int(line.split(':')[1].strip())
    except ValueError:
        raise ParserError(f'Invalid number of drones at line {current_line}')
    except IndexError:
        raise ParserError(f'Invalid line in your config file (line {current_line})')
    except Exception as e:
        raise ParserError(f'Could not parse your config file at line {current_line}: {e}')
    return nb_drones

def get_start_hub(line: str, current_line: str) -> Hub:
    """ Given a line from the configuration file, returns a Zone object corresponding to the start_hub """
    color = Color.DEFAULT
    restriction = ZoneRestriction.NORMAL
    max_drones = None

    try:
        start_hub = {
            'name': line.split(' ')[1],
            'x': int(line.split(' ')[2]),
            'y': int(line.split(' ')[3]),
        }
        line = line.split('[')[1].split(']')[0]
        for tag in line.split(' '):
            # If the tag is a color
            if tag.split('=')[0] == 'color':
                color = tag.split('=')[1]
            # If the tag is a restriction
            if tag.split('=')[0] == 'zone':
                restriction = tag.split('=')[1]
            # If the tag is a max_drone criteria
            if tag.split('=')[0] == 'max_drones':
                max_drones = tag.split('=')[1]
    except IndexError:
        raise ParserError(f'Corrupted start hub at line {current_line}')
    except ValueError:
        raise ParserError(f'Invalid coordinate at line {current_line}')
    except Exception as e:
        raise ParserError(f'Invalid configuration at line {current_line} -> {e}')
    try:
        hub = Hub(type=HubType.START_HUB, name=start_hub['name'], x=start_hub['x'], y=start_hub['y'],
                color=color, max_drone=max_drones, restriction=restriction)
    except Exception as e:
        raise ParserError(f'Invalid configuration at line {current_line} -> {e}')
    return hub

def get_normal_hub(line: str, current_line: str) -> Hub:
    """ Given a line from the configuration file, returns a Zone object corresponding to the normal hub """
    color = Color.DEFAULT
    restriction = ZoneRestriction.NORMAL
    max_drones = None

    try:
        normal_hub = {
            'name': line.split(' ')[1],
            'x': int(line.split(' ')[2]),
            'y': int(line.split(' ')[3]),
        }
        line = line.split('[')[1].split(']')[0]
        for tag in line.split(' '):
            # If the tag is a color
            if tag.split('=')[0] == 'color':
                color = tag.split('=')[1]
            # If the tag is a restriction
            if tag.split('=')[0] == 'zone':
                restriction = tag.split('=')[1]
            # If the tag is a max_drone criteria
            if tag.split('=')[0] == 'max_drones':
                max_drones = tag.split('=')[1]
    except IndexError:
        raise ParserError(f'Corrupted start hub at line {current_line}')
    except ValueError:
        raise ParserError(f'Invalid coordinate at line {current_line}')
    except Exception as e:
        raise ParserError(f'Invalid configuration at line {current_line} -> {e}')
    try:
        hub = Hub(type=HubType.HUB, name=normal_hub['name'], x=normal_hub['x'], y=normal_hub['y'],
                color=color, max_drone=max_drones, restriction=restriction)
    except Exception as e:
        raise ParserError(f'Invalid configuration at line {current_line} -> {e}')
    return hub

def get_end_hub(line: str, current_line: str) -> Hub:
    """ Given a line from the configuration file, returns a Zone object corresponding to the end_hub """
    color = Color.DEFAULT
    restriction = ZoneRestriction.NORMAL
    max_drones = None

    try:
        end_hub = {
            'name': line.split(' ')[1],
            'x': int(line.split(' ')[2]),
            'y': int(line.split(' ')[3]),
        }
        line = line.split('[')[1].split(']')[0]
        for tag in line.split(' '):
            # If the tag is a color
            if tag.split('=')[0] == 'color':
                color = tag.split('=')[1]
            # If the tag is a restriction
            if tag.split('=')[0] == 'zone':
                restriction = tag.split('=')[1]
            # If the tag is a max_drone criteria
            if tag.split('=')[0] == 'max_drones':
                max_drones = tag.split('=')[1]
    except IndexError:
        raise ParserError(f'Corrupted start hub at line {current_line}')
    except ValueError:
        raise ParserError(f'Invalid coordinate at line {current_line}')
    except Exception as e:
        raise ParserError(f'Invalid configuration at line {current_line} -> {e}')
    try:
        hub = Hub(type=HubType.end_hub, name=end_hub['name'], x=end_hub['x'], y=end_hub['y'],
                color=color, max_drone=max_drones, restriction=restriction)
    except Exception as e:
        raise ParserError(f'Invalid configuration at line {current_line} -> {e}')
    return hub

def parse(config_path: str):
    try:
        with open(config_path, 'r') as f:
            data = {
                'hubs': []
            }
            current_line = 0
            for line in f:
                current_line += 1
                line = line.split('#')[0]
                
                # Parsing number of drones
                if (line.startswith('nb_drones')):
                    nb_drones = get_nb_drones(line, current_line)
                    if 'nb_drones' not in data.keys():
                        data['nb_drones'] = nb_drones
                    else:
                        raise ParserError(f'Illegal redefinition of nb_drones in the configuration file at line {current_line}.')
                    continue

                # Parsing start_hub
                if (line.startswith('start_hub')):
                    print(line)
                    hub = get_start_hub(line, current_line)
                    if 'start_hub' not in data.keys():
                        data['start_hub'] = hub
                    else:
                        raise ParserError(f'Illegal redefinition of start_hub in the configuration file at line {current_line}.')
                    continue
                
                # Parsing hub
                if (line.startswith('hub')):
                    print(line)
                    hub = get_normal_hub(line, current_line)
                    data['hubs'].append(hub)
                    continue

                # Parsing end_hub
                if (line.startswith('end_hub')):
                    print(line)
                    try:
                        end_hub = {
                            'name': line.split(' ')[1],
                            'x': int(line.split(' ')[2]),
                            'y': int(line.split(' ')[3]),
                            'tags': []
                        }
                        line = line.split('[')[1].split(']')[0]
                        for tag in line.split(' '):
                            end_hub['tags'].append(
                                {
                                    tag.split('=')[0] : tag.split('=')[1]
                                }
                            )
                    except IndexError:
                        raise ParserError(f'Corrupted start hub at line {current_line}')
                    except ValueError:
                        raise ParserError(f'Invalid coordinate at line {current_line}')
                    except Exception as e:
                        raise ParserError(f'Invalit configuration at line {current_line} -> {e}')
                    if 'end_hub' not in data.keys():
                        data['end_hub'] = end_hub
                    else:
                        raise ParserError(f'Illegal redefinition of end_hub in the configuration file at line {current_line}.')
                    print(line)
                    print(end_hub)
                    continue
            
            if 'nb_drones' not in data.keys():
                raise ParserError('The configuration file doesn\'t specify a number of drones.')
            # VERIFIER QUE LE CHEMIN start_hub->end_hub est possible
            # print(data)
            # for keys in data.keys():
            #     print(data[keys])
            # for h in data['hubs']:
            #     print(h)
            print('------------')
            # hub = get_start_hub('start_hub: start 0 0 [color=red max_drones=15 zone=priority]', 42)
            for hubs in data['hubs']:
                hubs.print_data()
                print('')

    except FileNotFoundError as e:
        raise FileNotFoundError(f'The configuration file was not found: {e}')
