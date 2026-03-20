# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/19 22:27:03 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from src import ConfigParser, StateVisualizer, PathFinder


def main():
    parser = ConfigParser()
    visualizer = StateVisualizer()

    state = parser.parse_config_file("maps/hard/02_capacity_hell.txt")
    print(state)
    pf = PathFinder()
    target = state.zones[0]

    for z in state.zones:
        if z.drones != []:
            for drone in z.drones:
                state = PathFinder.move_drone(state, drone, target)

    visualizer.visualize(state)
    pass


if __name__ == "__main__":
    main()
