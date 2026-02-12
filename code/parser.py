#!/usr/bin/python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parser.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/11 13:52:30 by gtourdia        #+#    #+#               #
#  Updated: 2026/02/12 12:11:22 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from Zone import Zone, HubType, ZoneRestriction


def parse_mapping_file(input_path: str):
    output = {}
    output['hub_list'] = []
    available_hubtypes = tuple(item.value for item in HubType)

    # ? Opening input file
    try:
        f = open(input_path, 'r')
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The provided mapping file was not found. ({e})")
    except Exception as e:
        try:
            f.close()
        except Exception:
            pass
        raise Exception(f"Unable to load the mapping file ({e})")

    # ? Parsing lines
    for line in f:
        # Ignore comment
        line = line.split('#')[0]

        if line.startswith('nb_drones:'):
            try:
                nb_drones = int(line.split(':')[1])
            except ValueError as e:
                raise ValueError(f'Could not convert "nb_drones": ({e})')
            except Exception as e:
                raise Exception(f"Unable to access the value for nb_drones ({e})")
            output['nb_drones'] = int(nb_drones)

        elif line.startswith(available_hubtypes):
            metadatas = line.split('[')[1].replace(']', '').replace('\n', '')
            line = line.split(' ')
            # type: name x y [criteria=value criteria2=value]

            try:
                hub_type = line[0].strip(':')
                hub_name = line[1]
                x = line[2]
                y = line[3]
                color = None
                max_drone = -1
                restriction = ZoneRestriction.NORMAL
                
                # Getting 
                for metadata in metadatas.split(' '):
                    if metadata.split('=')[0] == 'color':
                        color = metadata.split('=')[1]
                    if metadata.split('=')[0] == 'max_drones':
                        max_drone = metadata.split('=')[1]
                    if metadata.split('=')[0] == 'zone':
                        restriction = metadata.split('=')[1]
                
                # Creating Zone object                
                output['hub_list'].append(
                    Zone(
                        type=hub_type,
                        name=hub_name,
                        x=x,
                        y=y,
                        color=color,
                        max_drone=int(max_drone),
                        restriction=restriction
                    )
                )
            except Exception as e:
                print('ALERTE')
                raise Exception(e)
    


    return output