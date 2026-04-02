# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:24:12 by gtourdia        #+#    #+#               #
#  Updated: 2026/04/02 14:43:34 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import ValidationError

from src.misc.arguments import get_arguments
from src.ConfigParser import ConfigParser
from src.StateVisualizer import AssetsException, StateVisualizer


def main() -> None:
    """
        Main script:
        - Parse the config
        - Lauch visualizer
    """

    # Get --input argument
    args = get_arguments()
    config_path = args.input

    try:
        # Parse config
        state = ConfigParser.parse(config_path)
    except ValidationError as e:
        print(f'Invalid configuration: {e.errors()[0]['msg']}')
        exit(0)
    except Exception as e:
        print(f'Configuration error: {e}.')
        exit(0)

    try:
        # Launch visualizer
        StateVisualizer.visualize(state)
    except AssetsException as e:
        print(f'Error in you assets: {e}')
        exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'An error occured: {e}, please contact gtourdia.')
