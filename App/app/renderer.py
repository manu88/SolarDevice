import pygame


SOURCE_RESOLUTION = (3840, 160)


class Renderer:
    def __init__(self):
        self.surface = pygame.Surface(SOURCE_RESOLUTION)
        self.test_surface = pygame.image.load("test.png")
        self.offset_inc = 50
        self.x_offset = 0
        self.paused = False

    def update(self):
        overflow = self.test_surface.get_width() - self.x_offset

        self.surface.blit(self.test_surface, dest=(self.x_offset, 0))
        self.surface.blit(self.test_surface, dest=(0, 0), area=(
            overflow, 0, self.x_offset, SOURCE_RESOLUTION[1]))

        if not self.paused:
            self.x_offset += self.offset_inc
            if self.x_offset >= self.test_surface.get_width():
                self.x_offset = 0
