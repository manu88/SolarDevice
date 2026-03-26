import pygame


SOURCE_RESOLUTION = (3840, 160)


class Renderer:
    def __init__(self):
        self.surface = pygame.Surface(SOURCE_RESOLUTION)
        self.test_surface = pygame.image.load("test.png")

    def update(self):
        self.surface.blit(self.test_surface, dest=(0, 0))
