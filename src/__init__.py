# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@42mulhouse.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:22:58 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/12 22:23:45 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

__version__ = '1.0.0'
__author__ = 'gtourdia'

# Errors
from .objects import ZoneConfigurationError, \
                    ConnectionConfigurationError, \
                    ConfigurationFileError

# Enumerations
from .objects import Color, \
                    ZoneType

# Main objects
from .objects import Zone, \
                    Drone, \
                    Connection, \
                    State

# Functions
from .parsing import parse_config_file

__all__ = [
    'ZoneConfigurationError',
    'ConnectionConfigurationError',
    'Color',
    'ZoneType',
    'Zone',
    'Drone',
    'Connection',
    'State',
    'parse_config_file'
    ]
