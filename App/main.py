from infoclimat.api import API
from display.display import Display
import pygame


def test_api():
    api = API()
    resp = api.get()
    assert resp
    weatherEntry = resp.get_current()
    print(weatherEntry)
    print(
        f"nebu: {weatherEntry.current_nebulosite()} -> {weatherEntry.next_nebulosite()}")


def test_display():
    pygame.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((640, 480))
    background = pygame.Surface(win.get_size())

    disp = Display()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        
        disp.update(background)
        win.blit(background, (0, 0))

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    test_display()
