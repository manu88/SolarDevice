from display.display import Display
import pygame


class App:
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
