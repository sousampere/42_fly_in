# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/27 17:35:19 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.MapState.Drone import Drone
from src.StateProcessor import StateProcessor
from src.ConfigParser import ConfigParser
from src.StateVisualizer import StateVisualizer

def main():
    config_path = 'maps/easy/02_simple_fork.txt'
    
    parser = ConfigParser()
    state = parser.parse(config_path)

    for zone in state.zones:
        print(zone.zone_type)
    
    # processor = StateProcessor()

    # for _ in processor.yield_process(state):
    #     pass

    state.connections[1].drones.append(Drone(name='danny'))

    visu = StateVisualizer()
    visu.visualize(state)

    print(state)

    pass


if __name__ == "__main__":
    main()
