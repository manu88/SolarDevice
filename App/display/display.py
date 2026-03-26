from typing import Tuple, Dict, Optional
import json
import pygame


WIDTH_PANEL = 320
HEIGHT_PANEL = 160


class Mapping:
    def __init__(self, screen_coords: Tuple[int, int], source_index: int):
        self.screen_coords = screen_coords
        self.flip_y = False
        self.source_index = source_index

    @staticmethod
    def from_data(data: Dict) -> 'Mapping':
        m = Mapping(screen_coords=(
            data["x"], data["y"]), source_index=data["source_index"])
        if "flip_y" in data:
            m.flip_y = bool(data["flip_y"])
        return m


class Display:
    def __init__(self, resolution: Tuple[int, int]) -> None:
        self.resolution = resolution
        self.num_panels = 12
        self.num_rows: int = -1
        self.num_cols: int = -1
        self.mapping: Dict[int, Mapping] = {}
        self.mire_surface: Optional[pygame.Surface] = None
        self._setup()

    def _setup(self):
        self.num_cols = self.resolution[0]//WIDTH_PANEL
        self.num_rows = self.resolution[1]//HEIGHT_PANEL
        index = 0
        for j in range(self.num_rows):
            for i in range(self.num_cols):
                x = i * WIDTH_PANEL
                y = j * HEIGHT_PANEL
                self.mapping[index] = Mapping(
                    screen_coords=(x, y), source_index=index)
                index += 1
        print(
            f"num_rows={self.num_rows} num_cols={self.num_cols} total panels={self.num_rows*self.num_cols}")
        for index, mapping in self.mapping.items():
            print(
                f"mapping i={index} sourcex={index*WIDTH_PANEL} to x={mapping.screen_coords[0]} y={mapping.screen_coords[1]}")

    def load_mire(self, file_path: str):
        self.mire_surface = pygame.image.load(file_path)

    def unload_mire(self):
        self.mire_surface = None

    def load_mapping(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            self.mapping = {}
            data = json.load(f)
            for idx, mapping_data in data["mapping"].items():
                index = int(idx)
                self.mapping[index] = Mapping.from_data(mapping_data)

    def _render_part(self, from_surface: pygame.Surface, to_surface: pygame.Surface, mapping: Mapping, screen_pos: Tuple[int, int], source_x: int):
        surf = pygame.transform.flip(
            from_surface, flip_x=0, flip_y=mapping.flip_y)
        to_surface.blit(surf, dest=screen_pos,
                        area=(source_x, 0, WIDTH_PANEL, HEIGHT_PANEL))

    def update(self, from_surface: pygame.Surface, to_surface: pygame.Surface, start_coords=(0, 0)):
        for mapping in self.mapping.values():
            x = start_coords[0] + mapping.screen_coords[0]
            y = start_coords[1] + mapping.screen_coords[1]
            pygame.draw.rect(to_surface, (0, 200, 255),
                             (x, y, WIDTH_PANEL, HEIGHT_PANEL), 1)
            source = self.mire_surface if self.mire_surface else from_surface

            self._render_part(from_surface=source, to_surface=to_surface, mapping=mapping, screen_pos=(
                x, y), source_x=mapping.source_index*WIDTH_PANEL)
