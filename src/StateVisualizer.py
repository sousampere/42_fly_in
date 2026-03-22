# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  StateVisualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/19 13:43:13 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/20 14:26:18 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
import pygame
import random
import sys

from src import State


class AbstractStateVisualizer(ABC):
    """Class to visualize a state"""
    @abstractmethod
    def visualize(state: State) -> None:
        pass


class StateVisualizer(AbstractStateVisualizer):
    @staticmethod
    def get_coords_range(state: State):
        """Returns the max/min for every axis of coords"""
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
        y_range = y_max - y_min
        x_range = x_max - x_min
        return {
            "x_max": x_max,
            "x_min": x_min,
            "y_max": y_max,
            "y_min": y_min,
            "y_range": y_range if y_range != 0 else 1,
            "x_range": x_range if x_range != 0 else 1,
        }
    
    @staticmethod
    def visualize(state: State):
        pass
        """Visualize a state"""
        # Setup
        pygame.init()
        WIDTH, HEIGHT = 2000, 1200
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fly-in to the mooon 🚀")
        drone = pygame.image.load("assets/drone.png").convert_alpha()
        pygame.display.set_icon(drone)

        # Constants
        BACKGROUND_COLOR = "#252422"
        TEXT_COLOR = "#0be62f"
        COLORS = ["green", "yellow", "red", "gray", "blue", "purple", "black", "brown"]

        # Loading assets
        pause_button = pygame.image.load("assets/pause.png").convert_alpha()
        play_button = pygame.image.load("assets/play.png").convert_alpha()

        pause_button = pygame.transform.scale(pause_button, (32, 32))
        play_button = pygame.transform.scale(play_button, (32, 32))
        interraction_container = pygame.Rect(10, 10, 200, 32)

        # Loading logo
        logo = pygame.image.load("assets/42_logo.png").convert_alpha()
        # logo = pygame.transform.scale(logo, (20, 20))
        logo_container = pygame.Rect(20, 20, WIDTH, HEIGHT)

        pause = False
        coords_range = StateVisualizer.get_coords_range(state)
        font = pygame.font.Font("assets/font.ttf")

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

            screen.fill(BACKGROUND_COLOR)

            pygame.draw.rect(screen, BACKGROUND_COLOR, interraction_container)
            pygame.draw.rect(screen, BACKGROUND_COLOR, logo_container)
            width_padding_percent = 0.8
            height_padding_percent = 0.6

            # Draw connections
            for zone in state.zones:
                zone_x = (zone.x - coords_range["x_min"]) * (
                    WIDTH * width_padding_percent
                ) / coords_range["x_range"] + WIDTH * ((1 - width_padding_percent) / 2)
                zone_y = (zone.y - coords_range["y_min"]) * (
                    HEIGHT * height_padding_percent
                ) / coords_range["y_range"] + HEIGHT * (
                    (1 - height_padding_percent) / 2
                )
                

                for connection in zone.connections:
                    zone_b = connection["zone"]
                    zone_b_x = (zone_b.x - coords_range["x_min"]) * (
                        WIDTH * width_padding_percent
                    ) / coords_range["x_range"] + WIDTH * (
                        (1 - width_padding_percent) / 2
                    )
                    zone_b_y = (zone_b.y - coords_range["y_min"]) * (
                        HEIGHT * height_padding_percent
                    ) / coords_range["y_range"] + HEIGHT * (
                        (1 - height_padding_percent) / 2
                    )
                    pygame.draw.line(
                        screen, TEXT_COLOR, (zone_x, zone_y), (zone_b_x, zone_b_y), 3
                    )

            # Draw zones circles
            for zone in state.zones:
                random.seed('seed')
                zone_x = (zone.x - coords_range["x_min"]) * (
                    WIDTH * width_padding_percent
                ) / coords_range["x_range"] + WIDTH * ((1 - width_padding_percent) / 2)
                zone_y = (zone.y - coords_range["y_min"]) * (
                    HEIGHT * height_padding_percent
                ) / coords_range["y_range"] + HEIGHT * (
                    (1 - height_padding_percent) / 2
                )

                pygame.draw.circle(screen, TEXT_COLOR, (zone_x, zone_y), 22)
                try:
                    pygame.draw.circle(screen, zone.color.value, (zone_x, zone_y), 20)
                except Exception:
                    pygame.draw.circle(screen, "white", (zone_x, zone_y), 20)

                img = font.render(zone.name, True, TEXT_COLOR)
                img_w, img_h = img.get_size()
                img = pygame.transform.scale(img, (img_w * 1.5, img_h * 1.5))
                if zone.x % 2 == 0:
                    screen.blit(img, (zone_x - img.get_width() / 2, zone_y - 50))
                else:
                    screen.blit(img, (zone_x - img.get_width() / 2, zone_y + 20))

                for drone in zone.drones:
                    drone_x = random.choice(range(int(zone_x) - 10, int(zone_x) + 10))
                    drone_y = random.choice(range(int(zone_y) - 10, int(zone_y) + 10))

                    pygame.draw.circle(screen, 'black', (drone_x, drone_y), 6)
                    pygame.draw.circle(screen, random.choice(COLORS), (drone_x, drone_y), 5)

            if pause:
                screen.blit(pause_button, interraction_container)
            else:
                screen.blit(play_button, interraction_container)

            screen.blit(logo, logo_container)
            img = font.render("./Fly-in_to_the_moon", True, TEXT_COLOR)
            img_w, img_h = img.get_size()
            img = pygame.transform.scale(img, (img_w * 5, img_h * 5))
            screen.blit(img, (WIDTH - img.get_width() - 30, 30))

            # Refresh frame
            pygame.display.flip()

        pygame.quit()
        sys.exit()