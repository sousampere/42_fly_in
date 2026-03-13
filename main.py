# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@42mulhouse.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/12 22:24:31 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src import parse_config_file


def main():
    parse_config_file("maps/easy/01_linear_path.txt")
    pass


if __name__ == "__main__":
    main()
