import pygame


def _draw_grid(surf: pygame.Surface, pos, res_panel, step=20):
    pygame.draw.rect(surf, (255, 0, 0),
                     (pos[0], pos[1], res_panel[0], res_panel[1]), 1)
    num_cols = res_panel[0]//step
    num_rows = res_panel[1]//step
    print(num_cols, num_rows)
    alternate = False

    for j in range(num_rows):
        for i in range(num_cols):
            x = pos[0] + i * step
            y = pos[1] + j * step

            draw = False
            if i % 2 == 0:
                draw = True
            if alternate:
                draw = not draw

            if draw:
                pygame.draw.rect(surf, (200, 200, 200),
                                 (x, y, step, step))
        alternate = not alternate


def gen_mire(res_panel=(320, 160), num_panels=12, out_file="mire.png"):
    size = (res_panel[0]*num_panels, res_panel[1])
    pygame.init()
    pygame.font.init()
    surface = pygame.Surface(size)
    font = pygame.font.SysFont(None, 160)
    for i in range(num_panels):
        pos_x = i*res_panel[0]
        _draw_grid(surface, (pos_x, 0), res_panel)
        text_surf = font.render(f'{i}', True, (255, 0, 0))
        surface.blit(text_surf, (pos_x+10, 10))

    pygame.image.save(surface, out_file)
