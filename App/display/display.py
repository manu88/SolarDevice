import pygame
from typing import Tuple
WIDTH_PANEL = 320
HEIGHT_PANEL = 160


class Display:
    def __init__(self, resolution: Tuple[int, int]) -> None:
        self.resolution = resolution
        self.num_panels = 12
        self.num_rows: int = -1
        self.num_cols: int = -1
        self._setup()

    def _setup(self):
        self.num_cols = self.resolution[0]//WIDTH_PANEL
        self.num_rows = self.resolution[1]//HEIGHT_PANEL
        print(
            f"num_rows={self.num_rows} num_cols={self.num_cols} total panels={self.num_rows*self.num_cols}")

    def update(self, surface: pygame.Surface, start_coords=(0, 0)):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                x = start_coords[0] + i * WIDTH_PANEL
                y = start_coords[1]+j * HEIGHT_PANEL
                pygame.draw.rect(surface, (0, 200, 255),
                                 (x, y, WIDTH_PANEL, HEIGHT_PANEL), 1)
