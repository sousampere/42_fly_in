

from abc import ABC, abstractmethod
import copy
from multiprocessing import process
import random

from pygame.cursors import arrow
from pygame.font import Font

from src.StateProcessor import StateProcessor
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
        WIDTH, HEIGHT = 2000, 1000
        ZONE_RADIUS = int(min(WIDTH, HEIGHT) * 0.015)
        sizes = (WIDTH, HEIGHT, ZONE_RADIUS)
        save_state = copy.deepcopy(state)
        turns = 0

        # Create screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        # Load textures
        block_tex = pygame.image.load('assets/dirt.bmp').convert()
        drone_tex = pygame.image.load('assets/drone_2.bmp').convert_alpha()
        arrow_tex = pygame.image.load('assets/arrow.bmp').convert_alpha()

        # Transform texture
        block_tex = pygame.transform.scale(block_tex, (64, 64))
        drone_tex = pygame.transform.scale(drone_tex, (ZONE_RADIUS * 2, ZONE_RADIUS * 2))
        drone_tex = pygame.transform.flip(drone_tex, flip_x=True, flip_y=False)
        arrow_tex = pygame.transform.scale(arrow_tex, (64, 64))

        # Create area to detect click, based on the arrow's dimensions
        arrow_rect = arrow_tex.get_rect(topleft=(0, 0))

        # Create background pattern

        # Init font
        font = pygame.font.Font('assets/font.ttf', 16)


        processor = StateProcessor()

        clock = pygame.time.Clock()
        running = True
        while running:
            sizes = pygame.display.get_surface().get_size()
            sizes = (sizes[0], sizes[1], ZONE_RADIUS)

            # Render background
            bg = StateVisualizer.create_background(block_tex, sizes)
            screen.blit(bg, (0,0))

            # Apply soft shadow filter
            shadow = StateVisualizer.get_transparency_filter(sizes)
            screen.blit(shadow, (0, 0))

            # Render Connections
            connections = StateVisualizer.create_connections(state, sizes, font)
            screen.blit(connections, (0, 0))

            # Render zones
            zones = StateVisualizer.create_zones(state, sizes, font)
            screen.blit(zones, (0, 0))

            # Render drones
            drones = StateVisualizer.create_drones(state, sizes, drone_tex)
            screen.blit(drones, (0, 0))

            # Render arrow
            screen.blit(arrow_tex, (0, 0))

            # Render controls
            controls = StateVisualizer.create_controls(sizes, font)
            screen.blit(controls, (arrow_tex.get_width() + 20, 0))

            # Render turns counter
            turns_text = font.render(str(turns), True, 'green')
            screen.blit(turns_text, (0, 0))

            # Update screen
            pygame.display.flip()
            clock.tick(60)  # Max 60 fps


            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        state = processor.process(state)
                        turns += 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        turns = 0
                        state = copy.deepcopy(save_state)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if arrow_rect.collidepoint(event.pos):
                        state = processor.process(state)
                        turns += 1

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
    def create_zones(state: State, sizes: tuple, font: Font):
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
            ) / max(1, (y_max - y_min)) + HEIGHT * (
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
            if zone.is_end:
                outline = 'yellow'

            pygame.draw.circle(surface, 'black', (zone_x, zone_y), ZONE_RADIUS + 5)
            pygame.draw.circle(surface, outline, (zone_x, zone_y), ZONE_RADIUS + 4)
            pygame.draw.circle(surface, 'black', (zone_x, zone_y), ZONE_RADIUS + 2)

            pygame.draw.circle(surface, color, (zone_x, zone_y), ZONE_RADIUS)


            # Render name of zone
            zone_name = font.render(f'{zone.name} ({len(zone.drones)}/{zone.max_drones})', True, 'white', 'black')

            if zone.x % 2 == 0:
                surface.blit(zone_name, (zone_x - zone_name.get_width() / 2,
                                        zone_y - (20 + zone_name.get_height())))
            else:
                surface.blit(zone_name, (zone_x - zone_name.get_width() / 2,
                                        zone_y + 20))

        return surface

    @staticmethod
    def create_connections(state: State, sizes: tuple, font: Font):
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
                    ) / max(1, (y_max - y_min)) + HEIGHT * (
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
                    ) / max(1, (y_max - y_min)) + HEIGHT * (
                        (1 - height_padding_percent) / 2
                    )
                    zone_2 = (zone_x, zone_y)
                if zone_1 is not None and zone_2 is not None:
                    pygame.draw.line(surface, 'white', zone_1, zone_2, width=5)
                    text_surface = font.render(f'{connection.moving}/{connection.max_link_capacity}', True, 'white')
                    text_coords = ((max(zone_1[0], zone_2[0]) + min(zone_1[0], zone_2[0])) / 2,
                                   (max(zone_1[1], zone_2[1]) + min(zone_1[1], zone_2[1])) / 2)
                    surface.blit(text_surface, text_coords)
        return surface

    @staticmethod
    def create_drones(state: State, sizes: tuple, drone_tex: pygame.Surface):
        WIDTH, HEIGHT, ZONE_RADIUS = sizes
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill((0,0,0,0))  # Make background transparent
        x_min, x_max, y_min, y_max = state.get_min_max_coords()
        width_padding_percent = 0.8
        height_padding_percent = 0.7

        # Get a local random seed to prevend drone changing pos at each frame
        local_random = random.Random('fly-in will be done before 2026-27-03')

        for zone in state.zones:
            for drone in zone.drones:
                drone_x = (zone.x - x_min) * (
                    WIDTH * width_padding_percent
                ) / (x_max - x_min) + WIDTH * ((1 - width_padding_percent) / 2)
                drone_y = (zone.y - (y_min)) * (
                    HEIGHT * height_padding_percent
                ) / max(1, (y_max - y_min)) + HEIGHT * (
                    (1 - height_padding_percent) / 2
                )
                drone_coords = (drone_x - 10 + local_random.choice(range(-10, 10)),
                                drone_y - 10 + local_random.choice(range(-10, 10)))
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
    
    def create_controls(sizes: tuple, font: Font):
        WIDTH, HEIGHT, ZONE_RADIUS = sizes
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill((0,0,0,0))  # Make background transparent
        controls = [
                    {
                        'name': 'Reset simulation',
                        'key_name': 'ESCAPE  ',
                        'key': pygame.K_ESCAPE
                    },
                    {
                        'name': 'Next turn',
                        'key_name': 'SPACE  ',
                        'key': pygame.K_SPACE
                    }
                ]
        width_sum = 0

        for control in controls:
            key = font.render(f'{control['key_name']}', True, 'yellow', 'black')
            text = font.render(f'{control['name']}', True, 'white', 'black')
            surface.blit(key, (width_sum, 0))
            width_sum += key.get_width()
            surface.blit(text, (width_sum, 0))
            width_sum += text.get_width()
            width_sum += 20
        
        return surface