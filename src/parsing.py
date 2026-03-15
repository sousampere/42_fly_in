# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:22:28 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/15 15:58:37 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src import State, ConfigurationFileError, ZoneType, Zone

# def parse_config_file(path: str) -> State:
#     """ Parse the configuration file to get the state of the field """
#     # Open and read file
#     with open(path, 'r') as f:
#         lines = f.readlines()

#     # Ignore comments
#     for line in lines:
#         line = line.split('#')[0]

#     # Parse content (setup)
#     nb_drones = None
#     start_hub = None
#     end_hub = None
#     zones = []
#     connections = []

#     # Get number of drones
#     for line in lines:
#         if line.startswith('nb_drones:'):
#             nb_drones = int(line.split(':')[1].strip())
#     if nb_drones is None:
#         raise ConfigurationFileError('Your configuration file doesn\'t'
#                                      ' have a set number of drones.')
    
#     # Get start_hub
#     for line in lines:
#         if line.startswith('start_hub:'):
#             line_split = line.split('[')[0].split(' ')
#             data = {
#                 'name': line_split[1],
#                 'x': line_split[2],
#                 'y': line_split[3],
#                 'color': None,
#                 'max_drones': 1,
#                 'zone': ZoneType.NORMAL
#             }
#             metadatas = line.split('[')[1].strip().strip('[]').split(' ')
#             try:
#                 for metadata in metadatas:
#                     metadata = metadata.split('=')
#                     if metadata[0] == 'color':
#                         data['color'] = metadata[1]
#                     if metadata[0] == 'max_drones':
#                         data['max_drones'] = int(metadata[1])
#                     if metadata[0] == 'zone':
#                         data['zone'] = metadata[1]
#             except Exception:
#                 raise Exception(f'Invalid configuration line : {line}. '
#                                 'Please refer to the examples to provide'
#                                 ' a valid configuration.')
#             start_hub = Zone(
#                 name=data['name'],
#                 x=data['x'],
#                 y=data['y'],
#                 type=data['zone'],
#                 color=data['color'],
#                 max_drones=data['max_drones'],
#                 is_end_hub=False)
    
#     if start_hub is None:
#         raise ConfigurationFileError('Your configuration file doesn\'t'
#                                      ' have a start hub.')

#     # Get the other hubs
#     for line in lines:
#         if line.startswith('hub:') or line.startswith('end_hub:'):
#             line_split = line.split('[')[0].split(' ')
#             data = {
#                 'name': line_split[1],
#                 'x': line_split[2],
#                 'y': line_split[3],
#                 'color': None,
#                 'max_drones': 1,
#                 'zone': ZoneType.NORMAL
#             }
#             metadatas = line.split('[')[1].strip().strip('[]').split(' ')
#             try:
#                 for metadata in metadatas:
#                     metadata = metadata.split('=')
#                     if metadata[0] == 'color':
#                         data['color'] = metadata[1]
#                     if metadata[0] == 'max_drones':
#                         data['max_drones'] = int(metadata[1])
#                     if metadata[0] == 'zone':
#                         data['zone'] = metadata[1]
#             except Exception:
#                 raise Exception(f'Invalid configuration line : {line}. '
#                                 'Please refer to the examples to provide'
#                                 ' a valid configuration.')
#             if line.startswith('hub:'):
#                 zones.append(Zone(
#                 name=data['name'],
#                 x=data['x'],
#                 y=data['y'],
#                 type=data['zone'],
#                 color=data['color'],
#                 max_drones=data['max_drones'],
#                 is_end_hub=False))
#             else:
#                 end_hub = Zone(
#                 name=data['name'],
#                 x=data['x'],
#                 y=data['y'],
#                 type=data['zone'],
#                 color=data['color'],
#                 max_drones=data['max_drones'],
#                 is_end_hub=True)
    
#     # Get connections
#     for line in lines:
#         if line.startswith('connection:'):
#             line_split = line.split(' ')
            

#     print(end_hub)