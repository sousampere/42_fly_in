# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/30 17:03:58 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.MapState.Drone import Drone
from src.StateProcessor import StateProcessor
from src.ConfigParser import ConfigParser
from src.StateVisualizer import StateVisualizer

def main():
    configs = [
        'maps/easy/01_linear_path.txt', # 3 turns
        'maps/easy/02_simple_fork.txt', # 3 turns
        'maps/easy/03_basic_capacity.txt', # 
        'maps/medium/01_dead_end_trap.txt',
        'maps/medium/02_circular_loop.txt',
        'maps/medium/03_priority_puzzle.txt',
        'maps/hard/01_maze_nightmare.txt',
        'maps/hard/02_capacity_hell.txt',
        'maps/hard/03_ultimate_challenge.txt',
        'maps/challenger/01_the_impossible_dream.txt',
    ]
    config_path = configs[2]
    # config_path = 'maps/medium/03_priority_puzzle.txt'
    
    parser = ConfigParser()
    state = parser.parse(config_path)

    for zone in state.zones:
        print(zone.zone_type)
    
    processor = StateProcessor()
    # state = StateProcessor.move_drone(state, 'D1', state.connections[0], state.zones[1])
    # state = processor.move_drone(state, 'D1', state.zones[1], going_to=state.zones[0])
    # print(processor.calculate_shortest_path(state, 'D1'))
    # state.connections[1].drones.append(Drone(name='danny'))

    visu = StateVisualizer()
    visu.visualize(state)

    print(state)

    pass


if __name__ == "__main__":
    main()
