import pygame, spritesheet, pyganim
from level_gen import map_gen

pygame.init()

debug = 0
size = (win_width, win_height) = (640, 360)

screen_rect = pygame.Rect(0, 0, win_width, win_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Golf Rush")
framerate = 60
framecount = 0
timer = pygame.time.Clock()

platformcolor = (0x994422)
bgcolor = (0, 0, 0)
alpha = (211, 249, 188) # 0xD3F9BC

bgsheet = spritesheet.spritesheet("bg.png")
bg = bgsheet.image_at((0, 0, 2000, 992), bgcolor)

tile_size = 32
tilesheet = spritesheet.spritesheet("tileset_ruins.png")
tileset = [[tilesheet.image_at(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size), alpha) for x in range(3)] for y in range(3)]

ballsheet = spritesheet.spritesheet("balls.png")
ball_golf = ballsheet.image_at((1, 1, 16, 16), alpha)
ball_poke = ballsheet.image_at((18, 1, 16, 16), alpha)

sheet_fx = spritesheet.spritesheet("fx.png")
fx_explosion_ground_big = pyganim.PygAnimation([(sheet_fx.image_at((1 + x,   1,  85,  54), alpha), 0.1) for x in range(0, 11,  86)])
fx_explosion_normal_big = pyganim.PygAnimation([(sheet_fx.image_at((1 + x,  58, 100,  84), alpha), 0.1) for x in range(0,  8, 101)])
fx_explosion_aerial_big = pyganim.PygAnimation([(sheet_fx.image_at((1 + x, 145, 100, 100), alpha), 0.1) for x in range(0,  8, 101)])
fx_explosion_ground = pyganim.PygAnimation([(sheet_fx.image_at((1 + x, 248, 52,  33), alpha), 0.1) for x in range(0, 11, 86)])
fx_explosion_normal = pyganim.PygAnimation([(sheet_fx.image_at((1 + x, 284, 63,  84), alpha), 0.1) for x in range(0,  8, 64)])
fx_explosion_aerial = pyganim.PygAnimation([(sheet_fx.image_at((1 + x, 340, 70, 100), alpha), 0.1) for x in range(0,  8, 71)])
fx_dust_large = pyganim.PygAnimation([(sheet_fx.image_at((1 + x, 413, 26, 25), alpha), 0.1) for x in range(0,  6, 26)])
fx_dust_small = pyganim.PygAnimation([(sheet_fx.image_at((1 + x, 441, 19, 11), alpha), 0.1) for x in range(0,  6, 20)])

level = map_gen(screen)
level_size = (level_width, level_height) = (len(level[0]) * tile_size, len(level) * tile_size)

input_down  = False
input_left  = False
input_up    = False
input_right = False
input_A     = False
input_B     = False

fullscr     = False

screenshake_frames = 0
screenshake_x = 0
screenshake_y = 0

sfx_jump = pygame.mixer.Sound("sfx_jump.wav")

class Tile(object):
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(x, y, tile_size, tile_size)
        
def make_level():
    tiles = []
    tile_x = 0
    tile_y = 0
    for row in level:
        tiles.append([])
        for char in row:
            if char.color == 1:
                tile = tileset[0][0]
            elif char.color == 2:
                tile = tileset[0][1]
            elif char.color == 3:
                tile = tileset[0][2]
            elif char.color == 4:
                tile = tileset[1][0]
            elif char.color == 5:
                tile = tileset[1][1]
            elif char.color == 6:
                tile = tileset[1][2]
            elif char.color == 7:
                tile = tileset[2][0]
            elif char.color == 8:
                tile = tileset[2][1]
            elif char.color == 9:
                tile = tileset[2][2]
            else:
                tile = None
            if tile is not None:
                tiles[tile_y].append(Tile(tile_x * tile_size, tile_y * tile_size, tile))
            else:
                tiles[tile_y].append(None)
            tile_x += 1
        tile_x = 0
        tile_y += 1
    return tiles

tiles = make_level()
