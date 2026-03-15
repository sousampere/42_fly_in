# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/15 16:04:22 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src import ConfigParser


def main():
    parser = ConfigParser()
    state = parser.parse_config_file('maps/easy/01_linear_path.txt')
    print(state)
    pass


if __name__ == "__main__":
    main()
