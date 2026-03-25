from infoclimat.api import API
from display.display import Display
from display.mire import gen_mire
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
    res = (1024, 640)
    pygame.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode(res)
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


if __name__ == "__main__":
    # gen_mire()
    test_display()
