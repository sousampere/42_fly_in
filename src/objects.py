#!/usr/bin/python3
# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  objects.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@42mulhouse.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 21:12:28 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/12 22:32:31 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from enum import Enum
from typing import List

from pydantic import BaseModel, Field, model_validator


# Errors
class ZoneConfigurationError(Exception):
    """ Zone Configuration Error """
    pass


class ConnectionConfigurationError(Exception):
    """ Connection Configuration Error """
    pass


# Enumerations
class Color(Enum):
    """ Enumeration of different colors possible """
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'
    GRAY = 'gray'
    BLUE = 'blue'


class ZoneType(Enum):
    """ Enumeration of different zone types possible """
    RESTRICTED = 'restricted'
    NORMAL = 'normal'
    PRIORITY = 'priority'
    BLOCKED = 'blocked'


class Drone(BaseModel):
    """ Drone object """
    name: str


# Main objects
class Zone(BaseModel):
    """ Zone object """
    color: Color = Field(default=None)
    name: str
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    type: ZoneType = Field(default=ZoneType.NORMAL)
    max_drones: int = Field(default=1, ge=0)
    drones: List[Drone] = Field(default=[])

    @model_validator(mode='after')
    def verify_data(self) -> "Zone":
        if '-' in self.name:
            raise ZoneConfigurationError(f'Invalid zone name {self.name}'
                                         '. A zone name can not contain '
                                         'dashes in its name.')


class Connection(BaseModel):
    """ Connection object that connects two zones """
    zone_one: Zone
    zone_two: Zone
    max_link_capacity: int = Field(default=1)
    drones: List[Drone] = Field(default=[])

    @model_validator(mode='after')
    def verify_data(self) -> "Connection":
        if (self.zone_one.name == self.zone_one.name):
            raise ConnectionConfigurationError('Tried to establish an '
                                               'invalid connection between'
                                               ' a zone and itself '
                                               f'({self.zone_one.name})')


class State(BaseModel):
    """ State of the operation
     Class containing zones and their connections """
    zones: List = Field(default=[])
    connection: List = Field(default=[])