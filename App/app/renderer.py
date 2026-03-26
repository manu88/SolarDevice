import pygame


SOURCE_RESOLUTION = (3840, 160)


class Renderer:
    def __init__(self):
        self.surface = pygame.Surface(SOURCE_RESOLUTION)

    def load_mire(self, file_path: str):
        s = pygame.image.load(file_path)
        assert s.get_size() == SOURCE_RESOLUTION
        self.surface.blit(s, dest=(0, 0))

    def update(self):
        pass
