import pygame


SOURCE_RESOLUTION = (3840, 160)


class Renderer:
    def __init__(self):
        self.surface = pygame.Surface(SOURCE_RESOLUTION)

    def update(self):
        pass
