from display.display import Display
import pygame
from pythonosc.dispatcher import Dispatcher
from app.osc_server import OSCServer


class App:
    def __init__(self, ip="127.0.0.1", port=5005):
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/foo", print)
        self.osc_server = OSCServer(self.dispatcher, ip=ip, port=port)

    def run(self):
        res = (1024, 640)
        pygame.init()
        clock = pygame.time.Clock()
        win = pygame.display.set_mode(res, pygame.RESIZABLE)
        background = pygame.Surface(win.get_size())

        disp = Display(res)
        loop = True
        disp.load_mapping("panels_conf.json")
        disp.load_mire("mire.png")
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            disp.update(background)
            win.blit(background, (0, 0))

            pygame.display.flip()
            clock.tick(10)

        self.osc_server.stop()
