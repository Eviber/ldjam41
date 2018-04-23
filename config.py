import sys, pygame, spritesheet, pyganim
from pygame import *
from level_gen import map_gen

pygame.init()
pygame.display.set_caption("Golf Rush")

class Gl:
    debug = 0
    size = (win_width, win_height) = (640, 360)

    screen_rect = pygame.Rect(0, 0, win_width, win_height)
    screen = pygame.display.set_mode(size)
    framerate = 60
    framecount = 0
    timer = pygame.time.Clock()


    #WE GODDA SHIPPIT
    #IT GOES OUT TOMORROW!!
    #BUT AHM NOT DUN WIT DA GRAPHIX!!!
    alpha = (211, 249, 188) # 0xD3F9BC
    platformcolor = (0x994422)
    bgcolor = (0, 0, 0)
    bgsheet = spritesheet.spritesheet("bg.png")
    bg = bgsheet.image_at((0, 0, 2000, 992), bgcolor)

    tile_size = 32
    level = map_gen(screen)
    level_size = (level_width, level_height) = (len(level[0]) * tile_size, len(level) * tile_size)

    fullscr = False

    input_down  = False
    input_left  = False
    input_up    = False
    input_right = False
    input_A     = False
    input_B     = False

    sheet_tiles = spritesheet.spritesheet("tileset.png")
    sheet_tiger = spritesheet.spritesheet("tiger.png")
    sheet_balls = spritesheet.spritesheet("balls.png")
    sheet_fx = spritesheet.spritesheet("fx.png")

    sfx_golf_hit  = pygame.mixer.Sound("sfx_golf_hit.wav")
    sfx_golf_miss = pygame.mixer.Sound("sfx_golf_miss.wav")
    sfx_land      = pygame.mixer.Sound("sfx_land.wav")
    sfx_tiger     = pygame.mixer.Sound("sfx_tiger.wav")

    @classmethod
    def toggle_fullscr(cls):
        cls.screen = pygame.display.set_mode(cls.size, 0 if cls.fullscr else FULLSCREEN)
        cls.fullscr = not cls.fullscr

    @classmethod
    def get_input(cls):
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN:
                if e.key in (K_ESCAPE, K_q):
                    sys.exit()
                if e.key == K_f or e.key == K_F11:
                    cls.toggle_fullscr()
                if e.key == K_UP:
                    cls.input_up = True
                if e.key == K_DOWN:
                    cls.input_down = True
                if e.key == K_LEFT:
                    cls.input_left = True
                if e.key == K_RIGHT:
                    cls.input_right = True
                if e.key == K_SPACE:
                    cls.input_A = True
                if e.key == K_LALT:
                    cls.input_B = True
            if e.type == KEYUP:
                if e.key == K_UP:
                    cls.input_up = False
                if e.key == K_DOWN:
                    cls.input_down = False
                if e.key == K_LEFT:
                    cls.input_left = False
                if e.key == K_RIGHT:
                    cls.input_right = False
                if e.key == K_SPACE:
                    cls.input_A = False
                if e.key == K_LALT:
                    cls.input_B = False

    @classmethod
    def set_tileset(cls):
        cls.tileset =[[cls.sheet_tiles.image_at(pygame.Rect(x * cls.tile_size, y * cls.tile_size, cls.tile_size, cls.tile_size), cls.alpha) for x in range(3)] for y in range(3)]

    @classmethod
    def set_tiles(cls, tiles):
        cls.camera = camera.Camera(cls.level_width, cls.level_height)
        cls.tiles = tiles

    @classmethod
    def set_balls(cls):
        cls.ball_golf = cls.sheet_balls.image_at((1, 1, 16, 16), cls.alpha)
        cls.ball_poke = cls.sheet_balls.image_at((18, 1, 16, 16), cls.alpha)

    @classmethod
    def set_fx(cls):
        cls.fx_explosion_ground_big = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x,   1,  85,  54), cls.alpha), 0.1) for x in range(0, 11,  86)])
        cls.fx_explosion_normal_big = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x,  58, 100,  84), cls.alpha), 0.1) for x in range(0,  8, 101)])
        cls.fx_explosion_aerial_big = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x, 145, 100, 100), cls.alpha), 0.1) for x in range(0,  8, 101)])
        cls.fx_explosion_ground = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x, 248, 52,  33), cls.alpha), 0.1) for x in range(0, 11, 86)])
        cls.fx_explosion_normal = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x, 284, 63,  84), cls.alpha), 0.1) for x in range(0,  8, 64)])
        cls.fx_explosion_aerial = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x, 340, 70, 100), cls.alpha), 0.1) for x in range(0,  8, 71)])
        cls.fx_dust_large = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x, 413, 26, 25), cls.alpha), 0.1) for x in range(0,  6, 26)])
        cls.fx_dust_small = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x, 441, 19, 11), cls.alpha), 0.1) for x in range(0,  6, 20)])


class Tile(object):
    def __init__(self, image, x, y):
        self.image = image
        self.rect = pygame.Rect(x, y, Gl.tile_size, Gl.tile_size)


def make_level():
    tiles = []
    tile_x = 0
    tile_y = 0
    for row in Gl.level:
        tiles.append([])
        for char in row:
            if char.color == 1:
                tile = Gl.tileset[0][0]
            elif char.color == 2:
                tile = Gl.tileset[0][1]
            elif char.color == 3:
                tile = Gl.tileset[0][2]
            elif char.color == 4:
                tile = Gl.tileset[1][0]
            elif char.color == 5:
                tile = Gl.tileset[1][1]
            elif char.color == 6:
                tile = Gl.tileset[1][2]
            elif char.color == 7:
                tile = Gl.tileset[2][0]
            elif char.color == 8:
                tile = Gl.tileset[2][1]
            elif char.color == 9:
                tile = Gl.tileset[2][2]
            else:
                tile = None
            if tile is None:
                tiles[tile_y].append(None)
            else:
                tiles[tile_y].append(Tile(tile, tile_x * Gl.tile_size, tile_y * Gl.tile_size))
            tile_x += 1
        tile_x = 0
        tile_y += 1
    return tiles



import camera

Gl.set_tileset()
Gl.set_tiles(make_level())
Gl.set_balls()
Gl.set_fx()
