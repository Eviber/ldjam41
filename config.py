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
