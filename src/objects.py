#!/usr/bin/python3
# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  objects.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 21:12:28 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/16 16:35:46 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from abc import ABC
from enum import Enum
from typing import Any, Dict, List
import pygame
import sys
from pydantic import BaseModel, Field, field_validator, model_validator



# Errors
class ZoneConfigurationError(Exception):
    """Zone Configuration Error"""

    pass


class ConnectionConfigurationError(Exception):
    """Connection Configuration Error"""

    pass


class ConfigurationFileError(Exception):
    """Connection Configuration Error"""

    pass


# Enumerations
class Color(Enum):
    """Enumeration of different colors possible"""

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    GRAY = "gray"
    BLUE = "blue"
    PURPLE = "purple"
    BLACK = "black"
    BROWN = "brown"
    ORANGE = "orange"
    MAROON = "maroon"
    GOLD = "gold"
    DARKRED = "darkred"
    VIOLET = "violet"
    CRIMSON = "crimson"
    RAINBOW = "rainbow"
    CYAN = "cyan"


class ZoneType(Enum):
    """Enumeration of different zone types possible"""

    RESTRICTED = "restricted"
    NORMAL = "normal"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Drone(BaseModel):
    """Drone object"""

    name: str

    def __str__(self):
        return self.name


# Main objects
class Zone(BaseModel):
    """Zone object"""

    color: Color = Field(default=None)
    name: str
    x: int = Field()
    y: int = Field()
    type: ZoneType = Field(default=ZoneType.NORMAL)
    max_drones: int = Field(default=1, ge=0)
    drones: List[Drone] = Field(default=[])
    is_end_hub: bool = Field(default=False)
    connections: List[Dict[str, Any]] = []

    @model_validator(mode="after")
    def verify_data(self) -> "Zone":
        if "-" in self.name:
            raise ZoneConfigurationError(
                f"Invalid zone name {self.name}"
                ". A zone name can not contain "
                "dashes in its name."
            )
        return self

    def __str__(self):
        return (
            f"Zone {self.name} at X:{self.x} & Y:{self.y}, "
            f"type {self.type.value}, {self.max_drones} max drones "
            f"of color {self.color.value}. Contains "
            f"{', '.join((map(lambda drone: str(drone), self.drones)))}. "
            f"Connections: {list(map(lambda c: c['zone'].name, self.connections))}"
        )

    def create_drones(self, number: int):
        drone_id = 1
        for _ in range(number):
            self.drones.append(Drone(name=f"drone_{drone_id}"))
            drone_id += 1


class State(BaseModel):
    """State of the operation
    Class containing zones and their connections"""

    zones: List[Zone] = Field(default=[])
    connection: List[Dict[str, Zone | int]] = Field(default=[])

    def __str__(self):
        zones = "\n".join(zone.__str__() for zone in self.zones)
        connections = "\n".join(c.__str__() for c in self.connection)
        string = f"=== BEGIN STATE ===\n{zones}\n{connections}\n=== END STATE ==="

        return string


class ConfigParser(ABC):
    @staticmethod
    def parse_config_file(path: str) -> State:
        """Parse the configuration file to get the state of the field"""
        # Open and read file
        with open(path, "r") as f:
            lines = f.readlines()

        # Ignore comments
        for line in lines:
            line = line.split("#")[0]

        # Parse content (setup)
        nb_drones = None
        start_hub = None
        end_hub = None
        zones: List[Zone] = []

        # Get number of drones
        for line in lines:
            if line.startswith("nb_drones:"):
                nb_drones = int(line.split(":")[1].strip())
        if nb_drones is None:
            raise ConfigurationFileError(
                "Your configuration file doesn't" " have a set number of drones."
            )

        # Get start_hub
        for line in lines:
            if line.startswith("start_hub:"):
                line_split = line.split("[")[0].split(" ")
                data = {
                    "name": line_split[1],
                    "x": line_split[2],
                    "y": line_split[3],
                    "color": None,
                    "max_drones": 1,
                    "zone": ZoneType.NORMAL,
                }
                metadatas = line.split("[")[1].strip().strip("[]").split(" ")
                try:
                    for metadata in metadatas:
                        metadata = metadata.split("=")
                        if metadata[0] == "color":
                            data["color"] = metadata[1]
                        if metadata[0] == "max_drones":
                            data["max_drones"] = int(metadata[1])
                        if metadata[0] == "zone":
                            data["zone"] = metadata[1]
                except Exception:
                    raise Exception(
                        f"Invalid configuration line : {line}. "
                        "Please refer to the examples to provide"
                        " a valid configuration."
                    )
                start_hub = Zone(
                    name=data["name"],
                    x=data["x"],
                    y=data["y"],
                    type=data["zone"],
                    color=data["color"],
                    max_drones=data["max_drones"],
                    is_end_hub=False,
                )
                start_hub.create_drones(nb_drones)

        if start_hub is None:
            raise ConfigurationFileError(
                "Your configuration file doesn't" " have a start hub."
            )

        # Get the other hubs
        for line in lines:
            if line.startswith("hub:") or line.startswith("end_hub:"):
                line_split = line.split("[")[0].split(" ")
                data = {
                    "name": line_split[1],
                    "x": line_split[2],
                    "y": line_split[3],
                    "color": None,
                    "max_drones": 1,
                    "zone": ZoneType.NORMAL,
                }
                metadatas = line.split("[")[1].strip().strip("[]").split(" ")
                try:
                    for metadata in metadatas:
                        metadata = metadata.split("=")
                        if metadata[0] == "color":
                            data["color"] = metadata[1]
                        if metadata[0] == "max_drones":
                            data["max_drones"] = int(metadata[1])
                        if metadata[0] == "zone":
                            data["zone"] = metadata[1]
                except Exception:
                    raise Exception(
                        f"Invalid configuration line : {line}. "
                        "Please refer to the examples to provide"
                        " a valid configuration."
                    )
                if line.startswith("hub:"):
                    zones.append(
                        Zone(
                            name=data["name"],
                            x=data["x"],
                            y=data["y"],
                            type=data["zone"],
                            color=data["color"],
                            max_drones=data["max_drones"],
                            is_end_hub=False,
                        )
                    )
                else:
                    end_hub = Zone(
                        name=data["name"],
                        x=data["x"],
                        y=data["y"],
                        type=data["zone"],
                        color=data["color"],
                        max_drones=data["max_drones"],
                        is_end_hub=True,
                    )

        zones.append(end_hub)
        zones.append(start_hub)

        # Connections
        for line in lines:
            if line.startswith("connection:"):
                line_split = line.split(" ")

                # Getting Zone A
                zone_a_name = line_split[1].split("-")[0].strip()
                zone_b_name = line_split[1].split("-")[1].strip()
                try:
                    max_link_capacity = line_split[1].strip("[]").split("=")[1]
                except Exception:
                    max_link_capacity = 1
                for zone_a in zones:
                    if zone_a.name == zone_a_name:
                        for zone_b in zones:
                            if zone_b.name == zone_b_name:
                                zone_a.connections.append(
                                    {
                                        "zone": zone_b,
                                        "max_link_capacity": max_link_capacity,
                                    }
                                )
                                zone_b.connections.append(
                                    {
                                        "zone": zone_a,
                                        "max_link_capacity": max_link_capacity,
                                    }
                                )

        state = State(zones=zones, connection=[])
        return state


class StateVisualizer(ABC):
    """Class to visualize a state"""

    @staticmethod
    def get_coords_range(state: State):
        """ Returns the max/min for every axis of coords """
        x_max = None
        x_min = None
        y_max = None
        y_min = None
        for zone in state.zones:
            if not x_max or zone.x > x_max:
                x_max = zone.x
            if not y_max or zone.y > y_max:
                y_max = zone.y
            if not x_min or zone.x < x_min:
                x_min = zone.x
            if not y_min or zone.y < y_min:
                y_min = zone.y
        return {
            'x_max': x_max,
            'x_min': x_min,
            'y_max': y_max,
            'y_min': y_min,
            'y_range': y_max - y_min,
            'x_range': x_max - x_min,
        }

    @staticmethod
    def visualize(state: State):
        """Visualize a state"""
        # Setup
        pygame.init()
        WIDTH, HEIGHT = 1200, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Fly-in to the mooon 🚀')
        drone = pygame.image.load('assets/drone.png').convert_alpha()
        pygame.display.set_icon(drone)

        # Loading assets
        pause_button = pygame.image.load('assets/pause.png').convert_alpha()
        play_button = pygame.image.load('assets/play.png').convert_alpha()
        
        pause_button = pygame.transform.scale(pause_button, (32, 32))
        play_button = pygame.transform.scale(play_button, (32, 32))
        interraction_container = pygame.Rect(10, 10, 200, 32)
        
        pause = False
        coords_range = StateVisualizer.get_coords_range(state)

        run_window = True
        while run_window:
            # Window close event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_window = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if interraction_container.collidepoint(event.pos):
                        if pause == False:
                            pause = True
                        else:
                            pause = False

            screen.fill('#1b263b')

            pygame.draw.rect(screen, '#1b263b', interraction_container)

            for zone in state.zones:
                try:
                    pygame.draw.circle(screen, zone.color.value, (
                        (zone.x - coords_range['x_min']) * (WIDTH * 0.8) / coords_range['x_range'] + WIDTH * 0.1,
                        (zone.y - coords_range['y_min']) * (HEIGHT * 0.6) / coords_range['y_range'] + HEIGHT * 0.2
                        ), 10)
                except Exception:
                    pygame.draw.circle(screen, 'white', (
                        (zone.x - coords_range['x_min']) * (WIDTH * 0.8) / coords_range['x_range'] + WIDTH * 0.1,
                        (zone.y - coords_range['y_min']) * (HEIGHT * 0.6) / coords_range['y_range'] + HEIGHT * 0.2
                        ), 10)
                for connection in zone.connections:
                    

            if pause:
                screen.blit(pause_button, interraction_container)
            else:
                screen.blit(play_button, interraction_container)
            

            pygame.display.flip()
            
        pygame.quit()
        sys.exit()