import os

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (10, 100, 240)
LVL200 = (247, 183, 159)
LVL300 = (126, 197, 84)
LVL400 = (83, 169, 64)
LVL500 = (253, 236, 83)
LVL600 = (233, 201, 56)
LVL700 = (225, 127, 52)
LVL800 = (172, 172, 172)
LVL900 = (126, 126, 126)
LVL950 = (255, 255, 255)
BGCOLOUR = BLUE

TILESIZE = 30
ROWS = 30
COLS = 33
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLS + 3
FPS = 60
TITLE = "Islands"
TEXT_SIZE = TILESIZE + 5

offset_X = 6
tile_X = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"x.png")),
                                (TILESIZE * 3 - offset_X, TILESIZE * 3 - offset_X))
tile_menu = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"menu.png")),
                                   (TILESIZE * 20, TILESIZE * 6))
tile_score_menu = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"menu.png")),
                                   (TILESIZE * 11, TILESIZE * 3 - 6))

MAX_LIVES = 3
FONT_NAME = 'Calibri'
