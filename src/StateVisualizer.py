

from abc import ABC, abstractmethod

from src.MapState import Drone
from src.MapState.State import State
import pygame


class AbstractStateVisualizer(ABC):
    @abstractmethod
    def visualize(state: State):
        pass


class StateVisualizer(AbstractStateVisualizer):
    @staticmethod
    def visualize(state: State):
        pygame.init()
        WIDTH, HEIGHT = 2000, 1200
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        block_tex = pygame.image.load('/home/gtourdia/Documents/42_fly_in/assets/dirt.jpg').convert()
        drone_tex = pygame.image.load('/home/gtourdia/Documents/42_fly_in/assets/drone_2.png').convert_alpha()
        block_tex = pygame.transform.scale(block_tex, (64, 64))
        drone_tex = pygame.transform.scale(drone_tex, (20, 20))
        bg = StateVisualizer.create_background(block_tex, WIDTH, HEIGHT)
        
        clock = pygame.time.Clock()
        running = True
        while running:
            
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Render background
            screen.blit(bg, (0,0))

            # Apply soft shadow filter
            shadow = StateVisualizer.get_transparency_filter(WIDTH, HEIGHT)
            screen.blit(shadow, (0, 0))

            # Render Connections
            connections = StateVisualizer.create_connections(state, WIDTH, HEIGHT)
            screen.blit(connections, (0, 0))

            # Render zones
            zones = StateVisualizer.create_zones(state, WIDTH, HEIGHT)
            screen.blit(zones, (0, 0))

            # Render drones
            drones = StateVisualizer.create_drones(state, WIDTH, HEIGHT, drone_tex)
            screen.blit(drones, (0, 0))

            # Update screen
            pygame.display.flip()
            clock.tick(60)  # Max 60 fps
    
    @staticmethod
    def create_background(texture: pygame.Surface, WIDTH: int, HEIGHT: int):
        bg = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        bg.fill((0,0,0,0))
        tile_w, tile_h = texture.get_size()
        for x in range(0, WIDTH, tile_w):
            for y in range(0, HEIGHT, tile_h):
                bg.blit(texture, (x, y))

        return bg

    @staticmethod
    def get_transparency_filter(WIDTH: int, HEIGHT: int) -> pygame.Surface:
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill((0,0,0,150))  # Make background transparent
        return surface

    @staticmethod
    def create_zones(state: State, WIDTH: int, HEIGHT: int):
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill((0,0,0,0))  # Make background transparent
        width_padding_percent = 0.8
        height_padding_percent = 0.7
        
        x_min, x_max, y_min, y_max = state.get_min_max_coords()

        # Draw zones
        for zone in state.zones:
            # Get responsive zone coords
            zone_x = (zone.x - x_min) * (
                WIDTH * width_padding_percent
            ) / (x_max - x_min) + WIDTH * ((1 - width_padding_percent) / 2)
            zone_y = (zone.y - (y_min)) * (
                HEIGHT * height_padding_percent
            ) / (y_max - y_min) + HEIGHT * (
                (1 - height_padding_percent) / 2
            )

            # Apply colors
            available_colors = pygame.color.THECOLORS.keys()
            color = zone.color if zone.color in available_colors else 'white'

            # Draw zones
            pygame.draw.circle(surface, color, (zone_x, zone_y), 15)

        return surface

    @staticmethod
    def create_connections(state: State, WIDTH: int , HEIGHT: int):
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill((0,0,0,0))  # Make background transparent
        x_min, x_max, y_min, y_max = state.get_min_max_coords()
        width_padding_percent = 0.8
        height_padding_percent = 0.7
        
        # Draw each connection
        for connection in state.connections:
            zone_1 = None
            zone_2 = None
            for zone in state.zones:
                # Zone 1 coord
                if zone.name == connection.zones[0]:
                    zone_x = (zone.x - x_min) * (
                        WIDTH * width_padding_percent
                    ) / (x_max - x_min) + WIDTH * ((1 - width_padding_percent) / 2)
                    zone_y = (zone.y - (y_min)) * (
                        HEIGHT * height_padding_percent
                    ) / (y_max - y_min) + HEIGHT * (
                        (1 - height_padding_percent) / 2
                    )
                    zone_1 = (zone_x, zone_y)
                # Zone 2 coord
                if zone.name == connection.zones[1]:
                    zone_x = (zone.x - x_min) * (
                        WIDTH * width_padding_percent
                    ) / (x_max - x_min) + WIDTH * ((1 - width_padding_percent) / 2)
                    zone_y = (zone.y - (y_min)) * (
                        HEIGHT * height_padding_percent
                    ) / (y_max - y_min) + HEIGHT * (
                        (1 - height_padding_percent) / 2
                    )
                    zone_2 = (zone_x, zone_y)
                if zone_1 is not None and zone_2 is not None:
                    pygame.draw.line(surface, 'white', zone_1, zone_2, width=5)
        return surface

    @staticmethod
    def create_drones(state: State, WIDTH: int , HEIGHT: int, drone_tex: pygame.Surface):
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill((0,0,0,0))  # Make background transparent
        x_min, x_max, y_min, y_max = state.get_min_max_coords()
        width_padding_percent = 0.8
        height_padding_percent = 0.7

        for zone in state.zones:
            for drone in zone.drones:
                drone_x = (zone.x - x_min) * (
                    WIDTH * width_padding_percent
                ) / (x_max - x_min) + WIDTH * ((1 - width_padding_percent) / 2)
                drone_y = (zone.y - (y_min)) * (
                    HEIGHT * height_padding_percent
                ) / (y_max - y_min) + HEIGHT * (
                    (1 - height_padding_percent) / 2
                )
                drone_coords = (drone_x, drone_y)
                surface.blit(drone_tex, drone_coords)

        return surface