# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/27 14:43:34 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.StateProcessor import StateProcessor
from src.ConfigParser import ConfigParser
from src.StateVisualizer import StateVisualizer

def main():
    config_path = 'maps/medium/02_circular_loop.txt'
    
    parser = ConfigParser()
    state = parser.parse(config_path)
    
    # processor = StateProcessor()

    # for _ in processor.yield_process(state):
    #     pass

    visu = StateVisualizer()
    visu.visualize(state)

    print(state)

    pass


if __name__ == "__main__":
    main()
