import pygame
from pythonosc.dispatcher import Dispatcher
from app.osc_server import OSCServer
from app.renderer import Renderer
from display.display import Display


class App:
    def __init__(self, conf_file_path: str, show_source: bool = False, ip="127.0.0.1", port=5005):
        self.show_source = show_source
        self.renderer = Renderer()
        pygame.init()
        res = (1024, 640)
        self.fps = 20
        self.disp = Display(res)

        if len(conf_file_path) > 0:
            self.disp.load_mapping(conf_file_path)

        self.win = pygame.display.set_mode(res, pygame.RESIZABLE)
        self.surface = pygame.Surface(self.win.get_size())

        self.dispatcher = Dispatcher()
        self.dispatcher.map("/mapping", self._on_mapping_msg)
        self.dispatcher.map("/save_mapping", self._on_save_mapping_msg)
        self.dispatcher.map("/load_mapping", self._on_load_mapping_msg)
        self.dispatcher.map("/mire", self._on_mire_msg)
        self.dispatcher.map("/pause", self._on_pause_msg)
        self.osc_server = OSCServer(self.dispatcher, ip=ip, port=port)

    def run(self):
        clock = pygame.time.Clock()

        loop = True
        try:
            while loop:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False

                self.update()
                self.win.blit(self.surface, (0, 0))

                pygame.display.flip()
                clock.tick(self.fps)
        finally:
            self.osc_server.stop()

    def _on_mire_msg(self, unused_addr, show: int):
        print(f"Show mire {show}")
        if show:
            self.disp.load_mire("mire.png")
        else:
            self.disp.unload_mire()

    def _on_save_mapping_msg(self, unused_addr, file_path: str):
        print(f"save mapping to file '{file_path}'")
        self.disp.save_mapping(file_path)

    def _on_load_mapping_msg(self, unused_addr, file_path: str):
        print(f"load mapping to file '{file_path}'")
        self.disp.load_mapping(file_path)

    def _on_mapping_msg(self, unused_addr, screen_idx: int, source_idx: int):
        print(
            f"on_mapping_msg screen_idx={screen_idx} source_idx={source_idx}")
        self.disp.mapping[screen_idx].source_index = source_idx

    def _on_pause_msg(self, unused_addr, pause: int):
        self.renderer.paused = bool(pause)

    def update(self):
        self.renderer.update()
        if self.show_source:
            ratio = (self.renderer.surface.get_size(
            )[0]//self.surface.get_size()[0]) + 1
            new_w = self.renderer.surface.get_size()[0]/ratio
            new_h = self.renderer.surface.get_size()[1]/ratio
            scaled = pygame.transform.scale(
                self.renderer.surface, (new_w, new_h))
            self.surface.blit(scaled, dest=(10, 0))
        else:
            self.disp.update(from_surface=self.renderer.surface,
                             to_surface=self.surface)
