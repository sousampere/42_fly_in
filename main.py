# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/24 14:38:46 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.StateProcessor import StateProcessor
from src.ConfigParser import ConfigParser

def main():
    config_path = 'maps/hard/02_capacity_hell.txt'
    
    parser = ConfigParser()
    state = parser.parse(config_path)
    
    processor = StateProcessor()

    for _ in processor.yield_process(state):
        pass

    print(state)

    pass


if __name__ == "__main__":
    main()
