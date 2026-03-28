# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/28 14:13:56 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.MapState.Drone import Drone
from src.StateProcessor import StateProcessor
from src.ConfigParser import ConfigParser
from src.StateVisualizer import StateVisualizer

def main():
    config_path = 'maps/medium/01_dead_end_trap.txt'
    
    parser = ConfigParser()
    state = parser.parse(config_path)

    for zone in state.zones:
        print(zone.zone_type)
    
    processor = StateProcessor()
    # state = processor.move_drone(state, 'D1', state.connections[1])
    # print(processor.calculate_shortest_path(state, 'D1'))

    # state.connections[1].drones.append(Drone(name='danny'))

    visu = StateVisualizer()
    visu.visualize(state)

    print(state)

    pass


if __name__ == "__main__":
    main()
