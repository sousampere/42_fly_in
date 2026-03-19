# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/19 12:33:40 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src import ConfigParser
from src.objects import StateVisualizer


def main():
    parser = ConfigParser()
    state = parser.parse_config_file('maps/hard/02_capacity_hell.txt')
    print(state)
    StateVisualizer.visualize(state)
    pass


if __name__ == "__main__":
    main()
