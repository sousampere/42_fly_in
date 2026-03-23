# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/23 14:20:46 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.ConfigParser import ConfigParser

def main():
    config_path = 'maps/hard/02_capacity_hell.txt'
    
    parser = ConfigParser()
    parser.parse(config_path)
    
    pass


if __name__ == "__main__":
    main()
