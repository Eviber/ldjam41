import sys, pygame, spritesheet, pyganim
from random import randint, seed
from pygame import *
from level_gen import map_gen

pygame.init()
pygame.display.set_caption("Golf Rush")
pygame.mixer.init(44000)

class Gl:
    debug = True
    size = (win_width, win_height) = (640, 360)

    screen_rect = pygame.Rect(0, 0, win_width, win_height)
    screen = pygame.display.set_mode(size)
    framerate = 60
    framecount = 0
    frameincr = 1 / (1000 / 60)
    timer = pygame.time.Clock()

    #WE GODDA SHIPPIT
    #IT GOES OUT TOMORROW!!
    #BUT AHM NOT DUN WIT DA GRAPHIX!!!
    alpha = (211, 249, 188) # 0xD3F9BC

    icon = pygame.image.load("icon.gif")
    pygame.display.set_icon(icon)

    img_tutorial = pygame.image.load("tutorial.png")
    img_ending = pygame.image.load("ending.png")

    bgcolor = (0, 0, 0)
    bgsheet = spritesheet.spritesheet("bg.png")
    bg = bgsheet.image_at((0, 0, 2000, 992), bgcolor)

    tile_size = 32
    fullscr = False

    level_finished = False

    input_down  = False
    input_left  = False
    input_up    = False
    input_right = False
    input_A     = False
    input_B     = False

    sheet_tiles = spritesheet.spritesheet("tileset.png")
    sheet_tiger = spritesheet.spritesheet("tiger.png")
    sheet_balls = spritesheet.spritesheet("balls.png")
    sheet_fx    = spritesheet.spritesheet("fx.png")
    sheet_load  = spritesheet.spritesheet("load.png")

    sfx_explosion   = pygame.mixer.Sound("sfx_explosion.wav")
    sfx_ball_bounce = pygame.mixer.Sound("sfx_ball_bounce.wav")
    sfx_golf_hit    = pygame.mixer.Sound("sfx_golf_hit.wav")
    sfx_golf_swing  = pygame.mixer.Sound("sfx_golf_swing.wav")
    sfx_jump        = pygame.mixer.Sound("sfx_jump.wav")
    sfx_land        = pygame.mixer.Sound("sfx_land.wav")
    sfx_tiger       = pygame.mixer.Sound("sfx_tiger.wav")

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
        cls.tileset = [[cls.sheet_tiles.image_at((x * cls.tile_size, y * cls.tile_size, cls.tile_size, cls.tile_size), cls.alpha) for x in range(3)] for y in range(3)]
        cls.goal_flag = cls.sheet_balls.image_at((1, 18, 32, 48), cls.alpha)

    @classmethod
    def set_camera_and_tiles(cls, tiles):
        cls.camera = camera.Camera(cls.level_width, cls.level_height)
        cls.tiles = tiles

    @classmethod
    def set_balls(cls):
        cls.ball_golf = cls.sheet_balls.image_at((4, 4, 10, 10), cls.alpha)
        cls.ball_golf_size = 10
        cls.ball_poke = cls.sheet_balls.image_at((18, 1, 16, 16), cls.alpha)
        cls.ball_poke_size = 16
        cls.ball_bomb = cls.ball_poke

    @classmethod
    def set_fx(cls):
        cls.fx = []
        cls.fx_explosion_ground_big = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x *  86,   1,  85,  54), cls.alpha), 0.06) for x in range(0, 11)], False)
        cls.fx_explosion_normal_big = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x * 101,  58, 100,  84), cls.alpha), 0.08) for x in range(0,  8)], False)
        cls.fx_explosion_aerial_big = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x * 101, 145, 100, 100), cls.alpha), 0.06) for x in range(0,  8)], False)
        cls.fx_explosion_ground = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x * 53, 248, 52,  33), cls.alpha), 0.06) for x in range(0, 11)], False)
        cls.fx_explosion_normal = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x * 64, 284, 63,  84), cls.alpha), 0.08) for x in range(0,  8)], False)
        cls.fx_explosion_aerial = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x * 71, 340, 70, 100), cls.alpha), 0.06) for x in range(0,  8)], False)
        cls.fx_dust_large  = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x * 27, 413, 26, 25), cls.alpha), 0.08) for x in range(0,  6)], False)
        cls.fx_dust_small  = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x * 20, 441, 19, 11), cls.alpha), 0.07) for x in range(0,  5)], False)
        cls.fx_dust_double = pyganim.PygAnimation([(cls.sheet_fx.image_at((1 + x * 55, 455, 54, 11), cls.alpha), 0.06) for x in range(0,  5)], False)

    @classmethod
    def play_fx(cls, anim, x, y, flip_x = False, flip_y = False):
        fx = Effect(cls)
        fx.play(anim, x, y, flip_x, flip_y)
        cls.fx.append(fx)

    @classmethod
    def update_fx(cls):
        for fx in cls.fx:
            fx.update()
            if fx.playing:
                cls.screen.blit(fx.image, cls.camera.apply(fx.rect))




class Effect(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.image = None
        self.rect = None
        self.anim = None
        self.playing = False
        self.flip_x = False
        self.flip_y = False

    def update(self):
        if self.playing:
            if self.anim.isFinished():
                self.image = None
                self.rect = None
                self.anim = None
                self.playing = False
            else:
                self.image = self.anim.getCurrentFrame()
                if self.flip_x or self.flip_y:
                    self.image = pygame.transform.flip(self.image, self.flip_x, self.flip_y)

    def play(self, anim, x, y, flip_x = False, flip_y = False):
        self.image = anim._images[0]
        self.rect = self.image.get_rect().move(x, y)
        self.anim = anim
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.anim.play()
        self.playing = True

class Tile(object):
    def __init__(self, image, x, y):
        self.image = image
        self.rect = pygame.Rect(x, y, Gl.tile_size, Gl.tile_size)

def make_level():
    while True:
        seed(time.get_ticks())
        Gl.seed = randint(0, 100000000)
        if not Gl.debug:
            try:
                Gl.level, (Gl.spawn_pos, Gl.goal_pos) = map_gen(Gl.screen, seed = Gl.seed)
            except Exception:
                continue
        else:
            Gl.level, (Gl.spawn_pos, Gl.goal_pos) = map_gen(Gl.screen, seed = 4201337) #seed = Gl.seed)
        Gl.level_size = (Gl.level_width, Gl.level_height) = (len(Gl.level[0]) * Gl.tile_size, len(Gl.level) * Gl.tile_size)
        print("seed -> ", Gl.seed)
        break

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
    tiles[Gl.goal_pos[1]][Gl.goal_pos[0]] = Tile(Gl.goal_flag, Gl.tile_size * Gl.goal_pos[0], Gl.tile_size * Gl.goal_pos[1])
    return tiles

import camera

Gl.set_tileset()
Gl.set_balls()
Gl.set_fx()
