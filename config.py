import pygame, spritesheet, pyganim
from level_gen import map_gen

debug = 0
size = (win_width, win_height) = (640, 360)
screen_rect = 0
screen = 0
framerate = 0
framecount = 0
timer = 0
platformcolor = 0
bgcolor = 0
bgsheet = 0
bg = 0
tile_size = 0
tilesheet = 0
tileset = 0
ballsheet = 0
img_ball = 0
level = []
level_size = 0
level_width = 0
level_height = 0
input_down  = 0
input_left  = 0
input_up    = 0
input_right = 0
input_A     = 0
input_B     = 0
fullscr     = 0
screenshake_frames = 0
screenshake_x = 0
screenshake_y = 0
alpha = 0
sheet = 0
anim_idle = 0
anim_walk = 0
anim_jumpcharge = 0
anim_jump = 0
anim_fall = 0
anim_golfcharge = 0
anim_golf = 0
sfx_jump = 0

pygame.init()

screen_rect = pygame.Rect(0, 0, win_width, win_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Golf Rush")
framerate = 60
framecount = 0
timer = pygame.time.Clock()

platformcolor = (0x994422)
bgcolor = (0, 0, 0)
bgsheet = spritesheet.spritesheet("bg.png")
bg = bgsheet.image_at((0, 0, 2000, 992), bgcolor)

tile_size = 32
tilesheet = spritesheet.spritesheet("tileset_ruins.png")
tileset = [[tilesheet.image_at(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)) for x in range(3)] for y in range(3)]

ballsheet = spritesheet.spritesheet("ball_golf.png")
img_ball = ballsheet.image_at((0, 0, 16, 16))

level = map_gen(screen)
print(level)
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

alpha = (211, 249, 188) # 0xD3F9BC

sheet = spritesheet.spritesheet("tiger.png")

anim_idle = sheet.image_at((  1,  1,64,64), alpha)
anim_walk = pyganim.PygAnimation([
        (sheet.image_at((  1, 66, 64, 64), alpha), 0.1),
        (sheet.image_at(( 66, 66, 64, 64), alpha), 0.1),
        (sheet.image_at((131, 66, 64, 64), alpha), 0.1),
        (sheet.image_at((196, 66, 64, 64), alpha), 0.1),
        (sheet.image_at((261, 66, 64, 64), alpha), 0.1),
        (sheet.image_at((326, 66, 64, 64), alpha), 0.1)])
anim_jumpcharge = [sheet.image_at((  1, 131, 64, 64), alpha),
            sheet.image_at(( 66, 131, 64, 64), alpha),
            sheet.image_at((131, 131, 64, 64), alpha)]
anim_jump = sheet.image_at((261,131,64,64), alpha)
anim_fall = sheet.image_at((326,131,64,64), alpha)
anim_golfcharge = [sheet.image_at((  1, 196, 64, 64), alpha),
            sheet.image_at(( 66, 196, 64, 64), alpha),
            sheet.image_at((131, 196, 64, 64), alpha),
            sheet.image_at((196, 196, 64, 64), alpha),
            sheet.image_at((261, 196, 64, 64), alpha),
            sheet.image_at((326, 196, 64, 64), alpha)]
anim_golf = [sheet.image_at(( 1, 261, 64, 64), alpha),
            sheet.image_at((66, 261, 64, 64), alpha)]

sfx_jump = pygame.mixer.Sound("sfx_jump.wav")
