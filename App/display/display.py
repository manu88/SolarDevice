import pygame
from typing import Tuple, Optional, Dict
WIDTH_PANEL = 320
HEIGHT_PANEL = 160


class Mapping:
    def __init__(self, screen_coords: Tuple[int, int], source_index: int):
        self.screen_coords = screen_coords


class Display:
    def __init__(self, resolution: Tuple[int, int]) -> None:
        self.resolution = resolution
        self.num_panels = 12
        self.num_rows: int = -1
        self.num_cols: int = -1
        self.mire_surf: Optional[pygame.Surface] = None
        self.panel_coords: Dict[int, Mapping] = {}
        self._setup()

    def _setup(self):
        self.num_cols = self.resolution[0]//WIDTH_PANEL
        self.num_rows = self.resolution[1]//HEIGHT_PANEL
        index = 0
        for j in range(self.num_rows):
            for i in range(self.num_cols):
                x = i * WIDTH_PANEL
                y = j * HEIGHT_PANEL
                self.panel_coords[index] = Mapping(
                    screen_coords=(x, y), source_index=index)
                index += 1
        print(
            f"num_rows={self.num_rows} num_cols={self.num_cols} total panels={self.num_rows*self.num_cols}")
        for index, mapping in self.panel_coords.items():
            print(
                f"mapping i={index} sourcex={index*WIDTH_PANEL} to x={mapping.screen_coords[0]} y={mapping.screen_coords[1]}")

    def load_mire(self, file_path: str):
        self.mire_surf = pygame.image.load(file_path)

    def _render_part(self, surface: pygame.Surface, screen_pos: Tuple[int, int], source_x: int):
        if self.mire_surf:
            surface.blit(self.mire_surf, dest=screen_pos,
                         area=(source_x, 0, WIDTH_PANEL, HEIGHT_PANEL))

    def update(self, surface: pygame.Surface, start_coords=(0, 0)):
        for index, mapping in self.panel_coords.items():
            x = start_coords[0] + mapping.screen_coords[0]
            y = start_coords[1] + mapping.screen_coords[1]
            pygame.draw.rect(surface, (0, 200, 255),
                             (x, y, WIDTH_PANEL, HEIGHT_PANEL), 1)

            self._render_part(surface, screen_pos=(
                x, y), source_x=index*WIDTH_PANEL)
