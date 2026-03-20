# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/20 14:37:32 by gtourdia        ###   ########.fr        #
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
            for drone in range(len(z.drones)):
                drone = z.drones[0]
                state = PathFinder.move_drone(state, z.drones[0], target)
    print(state)

    # print(type(state.zones[0].connections[0]['max_link_capacity']))
    # print(pf.get_drone_zone(state, drone))

    visualizer.visualize(state)
    pass


if __name__ == "__main__":
    main()
