import sys

import pygame
from pygame.math import Vector2 as _Vector
from pygame.mouse import get_pos as mouse_position
from pygame.mouse import get_pressed as mouse_buttons

from settings import *


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.origin = _Vector()
        self.pan_active = False
        self.pan_offset = _Vector()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)

    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = _Vector(mouse_position()) - self.origin
        if not mouse_buttons()[1]:
            self.pan_active = False

        if self.pan_active:
            self.origin = _Vector(mouse_position()) - self.pan_offset
        # mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50

    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        row = WINDOW_HEIGHT // TILE_SIZE

        for col in range(cols):
            x = self.origin.x + col * TILE_SIZE
            pygame.draw.line(self.display_surface, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

    def run(self, dt):
        self.event_loop()

        self.display_surface.fill('white')
        self.draw_tile_lines()
        
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
