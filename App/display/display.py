import pygame

WIDTH_PANEL = 320
HEIGHT_PANEL = 160


class Display:
    def __init__(self) -> None:
        self.num_panels = 12

    def update(self, surface: pygame.Surface):
        surface.fill((0, 200, 255))
