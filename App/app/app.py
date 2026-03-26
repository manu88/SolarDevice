import pygame
from pythonosc.dispatcher import Dispatcher
from app.osc_server import OSCServer
from display.display import Display


class App:
    def __init__(self, conf_file_path: str, ip="127.0.0.1", port=5005):
        pygame.init()
        res = (1024, 640)
        self.disp = Display(res)

        if len(conf_file_path) > 0:
            self.disp.load_mapping(conf_file_path)

        self.win = pygame.display.set_mode(res, pygame.RESIZABLE)
        self.surface = pygame.Surface(self.win.get_size())

        self.disp.load_mire("mire.png")
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/mapping", self._on_mapping_msg)
        self.osc_server = OSCServer(self.dispatcher, ip=ip, port=port)

    def run(self):
        clock = pygame.time.Clock()

        loop = True

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            self.disp.update(self.surface)
            self.win.blit(self.surface, (0, 0))

            pygame.display.flip()
            clock.tick(10)

        self.osc_server.stop()

    def _on_mapping_msg(self, unused_addr, screen_idx: int, source_idx: int):
        print(
            f"on_mapping_msg screen_idx={screen_idx} source_idx={source_idx}")
        self.disp.mapping[screen_idx].source_index = source_idx
