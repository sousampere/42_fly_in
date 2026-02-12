# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/11 13:51:15 by gtourdia        #+#    #+#               #
#  Updated: 2026/02/12 12:09:35 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from parser import parse_mapping_file


def main():
    try:
        parsing = parse_mapping_file('/home/gtourdia/Documents/42_fly_in/maps/hard/03_ultimate_challenge.txt')
        print()
        for _ in parsing['hub_list']:
            print('')
            _.print_data()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
