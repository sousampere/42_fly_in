

from abc import ABC, abstractmethod
import random

from src.MapState.Zone import ZoneType
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
        WIDTH, HEIGHT = 1200, 800
        ZONE_RADIUS = int(min(WIDTH, HEIGHT) * 0.015)
        sizes = (WIDTH, HEIGHT, ZONE_RADIUS)
        
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        block_tex = pygame.image.load('assets/dirt.bmp').convert()
        drone_tex = pygame.image.load('assets/drone_2.bmp').convert_alpha()
        block_tex = pygame.transform.scale(block_tex, (64, 64))
        drone_tex = pygame.transform.scale(drone_tex, (ZONE_RADIUS * 2, ZONE_RADIUS * 2))
        drone_tex = pygame.transform.flip(drone_tex, flip_x=True, flip_y=False)
        bg = StateVisualizer.create_background(block_tex, sizes)
        
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
            shadow = StateVisualizer.get_transparency_filter(sizes)
            screen.blit(shadow, (0, 0))

            # Render Connections
            connections = StateVisualizer.create_connections(state, sizes)
            screen.blit(connections, (0, 0))

            # Render zones
            zones = StateVisualizer.create_zones(state, sizes)
            screen.blit(zones, (0, 0))

            # Render drones
            drones = StateVisualizer.create_drones(state, sizes, drone_tex)
            screen.blit(drones, (0, 0))

            # Update screen
            pygame.display.flip()
            clock.tick(60)  # Max 60 fps
    
    @staticmethod
    def create_background(texture: pygame.Surface, sizes: tuple):
        WIDTH, HEIGHT, ZONE_RADIUS = sizes
        bg = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        bg.fill((0,0,0,0))
        tile_w, tile_h = texture.get_size()
        for x in range(0, WIDTH, tile_w):
            for y in range(0, HEIGHT, tile_h):
                bg.blit(texture, (x, y))

        return bg

    @staticmethod
    def get_transparency_filter(sizes: tuple) -> pygame.Surface:
        WIDTH, HEIGHT, ZONE_RADIUS = sizes
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill((0,0,0,150))  # Make background transparent
        return surface

    @staticmethod
    def create_zones(state: State, sizes: tuple):
        WIDTH, HEIGHT, ZONE_RADIUS = sizes
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
            if zone.zone_type == ZoneType.RESTRICTED:
                outline = 'red'
            elif zone.zone_type == ZoneType.BLOCKED:
                outline = 'black'
            elif zone.zone_type == ZoneType.PRIORITY:
                outline = 'green'
            else:
                outline = 'blue'

            pygame.draw.circle(surface, 'black', (zone_x, zone_y), ZONE_RADIUS + 5)
            pygame.draw.circle(surface, outline, (zone_x, zone_y), ZONE_RADIUS + 4)
            pygame.draw.circle(surface, 'black', (zone_x, zone_y), ZONE_RADIUS + 2)

            pygame.draw.circle(surface, color, (zone_x, zone_y), ZONE_RADIUS)

        return surface

    @staticmethod
    def create_connections(state: State, sizes: tuple):
        WIDTH, HEIGHT, ZONE_RADIUS = sizes
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
    def create_drones(state: State, sizes: tuple, drone_tex: pygame.Surface):
        WIDTH, HEIGHT, ZONE_RADIUS = sizes
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill((0,0,0,0))  # Make background transparent
        x_min, x_max, y_min, y_max = state.get_min_max_coords()
        width_padding_percent = 0.8
        height_padding_percent = 0.7
        random.seed('fly-in will be done before 2026-27-03')

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
                drone_coords = (drone_x - 10 + random.choice(range(-10, 10)),
                                drone_y - 10 + random.choice(range(-10, 10)))
                surface.blit(drone_tex , drone_coords)

        for connection in state.connections:
            for drone in connection.drones:
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
                
                drone_coords = ((max(zone_1[0], zone_2[0]) + min(zone_1[0], zone_2[0])) / 2 - 10,
                                (max(zone_1[1], zone_2[1]) + min(zone_1[1], zone_2[1])) / 2 - 10)

                surface.blit(drone_tex, drone_coords)

        return surface