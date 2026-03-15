# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 22:22:58 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/15 15:58:15 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

__version__ = '1.0.0'
__author__ = 'gtourdia'

# Errors
from .objects import ZoneConfigurationError, \
                    ConnectionConfigurationError, \
                    ConfigurationFileError, \
                    ConfigParser

# Enumerations
from .objects import Color, \
                    ZoneType

# Main objects
from .objects import Zone, \
                    Drone, \
                    Connection, \
                    State

__all__ = [
    'ZoneConfigurationError',
    'ConnectionConfigurationError',
    'ConfigurationFileError',
    'Color',
    'ZoneType',
    'Zone',
    'Drone',
    'Connection',
    'State',
    'ConfigParser'
    ]
