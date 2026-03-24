# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/24 13:17:26 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.ConfigParser import ConfigParser

def main():
    config_path = 'maps/hard/02_capacity_hell.txt'
    
    parser = ConfigParser()
    state = parser.parse(config_path)
    
    print(state)

    pass


if __name__ == "__main__":
    main()
