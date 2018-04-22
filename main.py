import sys, pygame
from pygame import *
from player import *

size = (win_width, win_height) = (640, 360)

bgcolor = (100, 150, 100)
platformcolor = (0x994422)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Golf Rush")
framerate = 60
framecount = 0
timer = pygame.time.Clock()

tile_size = 32
level = [
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111110001100000111111111111111110011111110001100111111111110000011111100000111110000111100011110001110001100111110000000000000000111111110000001111000110000000",
"1111111100000000111111111111000000000000000000001110000000000000111000000000000000000000000011100001110000110001111110000000000000000000000000000111000000000001",
"1111111110000000111111111111001100011100000111111110000000000000110000000000011000000000000000011000000000110001111110000011111111100000000000000000000000000001",
"1111111110000000001110000000001111111100001111100000000000000000000000011111111000000000000000011000000000000001111100000011000011100000011000000000000000011111",
"1110000000000000000000000000000001100000001111110000000000000000011110011111100000000000000110000000001100000000111100110001111111100000011000110011000000011111",
"1100000000000000000011110000000001100000000001110000000000000000011110000000000000000111111110000000001100000000111000110011110011100000000000110011000000011111",
"1111111000001111100011110001111000000000111001100001100000000001111111111000000000000111111110000000000000000000000000000011000000111000000000000000000000000000",
"1110011111001111110001111111111000001111111001111111111110000001100111111001110000000000000000000000001110000111110000001110000000111110000000000000000000000000",
"1100000111111111110001111111000000001111000001111100011110000000000111100001111111000000000000000000011110000111110000011111000000111111100000000000000000000000",
"1111100001111000000000011111000000001110000001111000011110000011100000000001100111001111111100000000011100000001100000011111000000000011111110000000000011000000",
"1111100001110000000000000000000000000000000000111000001110000011100000000000000110001111111100000000011100000000000000001110000000110000011110000000000011111111",
"1111100001110001100000000000000000000000000000000000000000111000000111000000000110001111111110000000011100000000000000001110000001111111110000000000000011111111",
"1100000000110001110000000000000000000001110000000000000000111111100111001110000000000000000111100000000000000000000000000000000001111111111111000011100011000011",
"1110000000111111111111000000011111110001111000000000000000111111100110001110000110011100011000110000000000111110000000000000001111111100011111000011100000000000",
"1110000000111100001111000000011111110001111000000000000000000011111111111100000111111110011111111110011100111110000000000000001111111000000110011001100111100000",
"1110000001111100000000000000000000111111001111000000111000000000001100000000000111111111111111111110011100110000001100011000001111111110000000011110000111100000",
"1100000001111100110000000000000000001111001111110000111000000000111100111111001100000000111111111110001100011100011100011110000110001110000000000110000000000001",
"1111001110000000110000000000000011000011000001110000000000001100111000111111001100000000000111111110000000001111110000011110000111111110000011111000000000000001",
"1111111111000000011001111100000011111111000000000000000000001100111000000000001100000000000000011110000000001111111110011111111111111110000011111111110000000000",
"1111111111000000011001111100000011110000000000000000111100001100111000001111100000000111111111100000000000001111111110000000111111111100000000000011110000000000",
"1111111111000000011111100000000011100001111000000000111100000000111000011001111100000111111111100000000000000111111110000000110000000000000000000000000000000000",
"1111001100000000000111100000000000001111111000000000000000110000000000011000001100000110000000000000000000000000000000001111110000000000000011000000000000000000",
"1110001100000111000001100000000000001110000000000000000000110000000000011000001100000000000000111000000000000000000000111110000000000000001111000000000000000000",
"1110000000000111111100011100000000001110000000000000000000000000000000011000110000000000000001111110000000000000000000111110000000000000111100000000000000000000",
"1100000000000111111100011100000110000000000000000000000000000000000000001100110000000000000001111110000000000000000000001110000011110000111100111110000000011000",
"1100000000000000000000000011111110000000000111100000000000000000000111111111110000000011110000000000000000000000000011111110000011110000000000111110000000011000",
"1100011000000000001110000011111110011000001111100001111111100000000111100000000000000011110000000000011000000000000111001100000000000000000000000000000000110000",
"1111111000000000001111000011110000011000011111100001111111100000000110000000000000000000110000001111111100011000001111000110000000011111111111111110000000111111",
"1100000000000000001111000000111111111111111100000000000000000000000000000000000000000000110000001111111100011111111110000110000001111111000000000011000001111111",
"1100111110000000001100000000001111111111111000000000000111000000000000001111111110000000000000000000001100011111110000000000000001110011000111000011000001110000",
"1100111111111000000011000000000000000000000000000000011111000000000000001111111110000000000111100000000000000000000000000000000000000111100111110000000000000000",
"1100110001111000000011000000000110000001111000000000111000000000000001111111100000000000000111110001100000000000000000000000000000000111100001110000000000000000",
"1100110000000000000000000000000111110001111000011111111000011100000001111111100000000000000000111111100000011000000000000011100000000111111100011100000000000001",
"1100000110001110000000011111000000111111100000011111110000011100000001100000000000000000000000000111100001111110000000000011100000000111001100011100000000000001",
"1111111110001110000000011111000011111110000000011100000000011100000001111111000111100000000000000000000111111110000000000000111000000111111110011100000000000001",
"1111111110000000000000001110000011111000000001111100000000000111100000000111000111100000000000000000000111100000000111100000011000000000001111000000000000000001",
"1100000111000000000000000000000111000000000011110000000000000011100000111110000001111110000000000000000111110000011111100000011000000000000001100001111111000000",
"1110000111000000000011000001100111000000000011110000000000000000000000111110000001111110000000111110000000111111111110000000000000000000001111111001111111000000",
"1111111111111110000011000111100111000111110000000000000000001111110000000111110000000000000001111110000000000111000000000000000000000000011111111000111111000000",
"1111000000000110000000000111000110000111111000000111111000001111110000111111111100000000000111111000000000000110000011100001100000011000011110000111111000000000",
"1111000111000000111100011111000110000000111000000111111110000000000000111100011111111000000111100000000000011111000011100001100000011100011110000111110000000001",
"1111000111000000111100011111000000000000110000000000001111110000000000001111111100111110000000001100000000011111111111100001111000011100000000000110001100001111",
"1110001111110001110000011111000000000000000000000000000011110000000110000000000111111110001100011100111000011111111111100001111000000000000000000011111100001111",
"1100011100011001100000000110000000000001100000000000000000110000000110011000000011111100001100011100111000000000000000000001111000000000110000000000001110000001",
"1100011000011111100000000011000000000001100000000000000011100000000000011000110000000000001100000000111000000000000111110001111000000000110011100000001110000111",
"1111111110000000000000011111110000000000000000000000000011000000000001111000110000000000000000000000000000000000000111110000000000000000000011100000001100001111",
"1110001110011000000000011000111111111110000000000000001100000000001111111000000000000000011110000000011000000000000000011110000000000000000011000111111100001111",
"1110000000011000000000000000111111111110000000001100001100000000011111111000000000110000011111000000011000111111100000011110000000000000111001111111100001111100",
"1110000110011000000000000000000001110000000110001100000000000000011000000000000000110000000001111000000011111111110000011000000111100000111111110000011111111100",
"1111100110011111110000000000001111111100000110000000000000000000000000000000000000000000000000011001111111111111110011111000000111100000000011111111111100110000",
"1111100000011111110000000001111100001100000000000000000000000000000111110000000000000000000111000001100000011111111111100000000000000000000011111111100000000000",
"1111100000000001110000000001100000000111000000000000000000000000000111111000000000000000000111000001100000011100011111100000000011000000000000001111100000000000",
"1111100000000000000000000000000111000111000000000000011111100000011110001110000000000000000011000001100000000000001110001100110011100000000000000000000000000011",
"1111100000000000000000000000001111000000000111110011111111111100011110001111100000000000111111000001100000000000000000001111110011100001100000000000000000000111",
"1111100000000000000000000000001111000000000111110011100000111100000000000001100000000000111000011000000000000000000000111110000011111111110000000000000000001111",
"1100000000011000000111000000000000000000000000110000000000000000000000000000000000000000000111111000000000000000011111111000000000011111111000000011110000001111",
"1110000000011111100111100000000000000111111000000000000000000000000000110000011000000000000111000000000000011001111111100000000000011111111110000011110000000001",
"1110000000000011100011111100000000000111111110000000000000000000000000110000011000111000000000000000000000011111110000000000011100000011111111000000000000000111",
"1100000000000000000000111100011100000000000110000011110000000011110000000000000000111111000000000000001100000000000000000000011100000011111111100000001100111111",
"1100000000000000000110001111111100000000000000000011110000000011110000000000000000111111000000000000001110000000000000001100000000000000000001100000001100111111",
"1111100000000000000110000111111000000000000001111111110000000011000110000000000000111111000000000000001111110000111111111110000000001100000001111000000000000000",
"1111100000000000000000000000011000000000000001111110000000000000000110000000000000000111000000000000000000110000111001100110000000001100000000111000011000110000",
"1100111000000000000001111100000000000000000001111100000000111100000110000000000000000011111100000000000000000000000001100110000000000000011001111000011000110001",
"1100011110000000011111111100000000000000000001111100001111111100000000000000000000000011111110011111111100000000000001100110000000000000011001111000000000000001",
"1111111111111111111110001100000000000111110000001111111111111000000000111100000000000000111110011111111110000000000000000000000000011000011111110000000000000000",
"1100011000111111000000000000000111111111110000000011111111111111110000111100011111110000111110000011111110000000000000000000110000011000001111000000000000000001",
"1110011000111111000000000000011111111111110000000001100000111111110000001111111111110000001100000110000000000110000000000001110000000000001110000000000001111111",
"1110000000110000000001100000011100000000000111111111111111111111000000001111111000000000000111111111111100000110000000000011110000000000000000000011110011001100",
"1110000000000000000001100000011111100000000111111100111110000011000000000011111111000000000111111110000111100110000000000011110000110000000000000011111111111100",
"1110000000000000000000000000011001110000000111111111111110000000000000000000011111000001111111111110000111100000000000000000000000110000011100000011111111111100",
"1100000000000011111000000011111111110000000000001111100000000000111000000000011000000011111111110000000000000110000001110000111100000001111100000000000001111111",
"1100000000000111111001100011111111000000000000000011100001111000111000001100011110000011111111000000000000011110000001110000111100000011110000000000000000000001",
"1100000000000111110011100011110000000000000000000000000001111000110000001111100110000011100000000000000000011000000001100000111100000011100000001100000000000011",
"1111110000000001111111000000000000011110001111111100000000000000110000000001111111110000000000000000000000000000110000000000000001110011100000001100011100000111",
"1111110000000000000111000000000000111111111111111100000000001110000000000111100111110000000000000000000011110000111000000000000001110000000000001100011100011111",
"1111100000000000001100000000000000111111111001111000001111111110000001111100000111110000000000000000000011110000111110000000000000000000000011000000000000011111",
"1110000000000000001110000000000000110000000011111100001111111110000001111000000001110000000000000000000000111100111110000000000000000000000011000000000011111100",
"1111000000000000001110000000000000111110001111111100000110000000111111000000000001110000000000000001110000111100000000000000000000000000000011000000000011111111",
"1111000000000000011000000011111100111111111111000000000000000111111110000000000000001100000000000001110000001100000000110000000000000000000000000000000000000011",
"1111000000000000011000000011111100000000000000000000000000000111000110000110000000001100000011000000000011111111000001110000000000000000000000000000000000011000",
"1111000000000110011100000111111100000000000000011111111100000000000110000110000000001100000011000000000111111111000001110000000000001110000000111000011100011001",
"1100000000000111111100011110000000000000000000011111111100000000000000000000000000000000000000000000001111110000000000000000000011111110000000111000111100000001",
"1111111100000111000000111110000000000000001100000111111000000000000000000000000011000111111000000000001111100110000000000000000011110000011000111000111110000001",
"1111111100000111111111111000001111000000001100000000000000011100000000000000000011000111111000000000011111001110000000000000000011110000011000000000011110000000",
"1100000000000111111111111110001111000001111110011000000000011100000000000000000000000000000000000000011111001110000000000011000011000111111000000000000000000000",
"1100000000000111111111111111100000110001111110011111100000000000011001100000000011110011111110000000000000000000000000000011000011100111111000000000000000000011",
"1100000000000000000000001111100000110001100110000001111111000000011001100000000011111111111110000000000000000111100011110000000001100000000000000011111000000011",
"1100000011100000000000001111100000000001100000000000001111000000000000000000000011111000000000000000000000000111100011111000000000000001111000000011111000000001",
"1100000011100000000000000111000000000001100000000001111000001111000001100000000000001111000000000000000000000110000011111000000000000111111110000000001100000000",
"1100000011100000000000000000000000000111100000011111111110001111000001111111111000001111000000000000000000000000000000001110000000000110001110000000000111110001",
"1111111001100000000011000000000000000110000000011000111110000011000000111000111000000000000000000000000000000000000000011110000111000000111111110000001100110001",
"1111111000000000000011000000000111000000000000000000111111110000000000011111110000000000000111000000000000000000000111111111100111000000110001111111111100000001",
"1110000000000000110001110000000111000001110000000000111111110000000000011111000000000000000111000000000000000000000111000111100001111111000000000001100000000001",
"1100000000000000110000111000000000000111110000000011110000110000000011111111000001100000000111110000000000000000000011000111100110011111100000000001111111000001",
"1100000000000011100000111000000110000111000000000111000000000011111111000011111001100000000111110000000000110000001110000000000111111111100001100000001111111111",
"1100000000011111100000000000000110000000000000000111000000001111111111100000111001111100000000000000001111110000001110000000000011001110001111111100000111111111",
"1110000000111000111100000000000000000000000000000000000011111111111111100000111000011111111100000000001110000000000000000000000011000000001111111111000011110000",
"1110000000111000011100000000000000000000000111000001111111111111000110000000000000011111111100000000011110000000000000000000000000000110000001111111000000000000",
"1110000011111000000000000000000000000011100111000001111100111110000000001100111000000000001100000000011110001110000000000000000000000110000000011000000000000000",
"1100011111111000000000000000011111000011100000000001111000111100000000011100111000110000000000000000000000111110000000000000111110000000000000011111100000000011",
"1100011000000000000000000111111111111111100000000000110000000000000000110000000000110000011000000000011111111110000000001100111110000000000000000011100011000011",
"1100001110000000000000001111001111000000000000000000000000000111000000110000000000011100011000000000011111000000001111001100000110000000000011111110000011000001",
"1111000110000000000000001100000111111111000000000000110000000111000000000000000000011100001111000000000000000000011111111100000110000000000011000000000011100001",
"1111000000000011100000000001111111000011000000000000110000000111000000000000011000000001111111000000000000000000011000000000000110000000000011000000000001111000",
"1111000111111111110000000001111110000111111111110000111000000000000000111100011000000111111111000000000000000000001100111111100000000000000000000000000000111000",
"1111000111111111110000110000000000001111111111110000111000000000001111111100000000000111111111000000000000000000011111111111100000001111110000000001100000000001",
"1100000000111000110000110000111000011111111111000001111100000000011111100001100000000000000111000000000000000000011110000000111000001111110000000001100011100001",
"1111000000111111100000000000111111111111111001110001111110000000011111110011111110000000000000000111111000111111000000000110011110000001111111100111110011111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
]
level_size = (level_width, level_height) = (len(level[0]) * tile_size, len(level) * tile_size)

input_down  = False
input_left  = False
input_up    = False
input_right = False
input_A     = False
input_B     = False

fullscr     = False
def toggle_fullscr():
    global fullscr
    global screen
    screen = pygame.display.set_mode(size, 0 if fullscr else FULLSCREEN)
    fullscr = not fullscr

screenshake_frames = 0
screenshake_x = 0
screenshake_y = 0
def screenshake(duration, force_x, force_y):
    global screenshake_frames
    global screenshake_x
    global screenshake_y
    screenshake_frames = duration
    screenshake_x = force_x
    screenshake_y = force_y

def get_input():
    global input_down
    global input_left
    global input_up
    global input_right
    global input_A
    global input_B
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == KEYDOWN:
            if e.key in (K_ESCAPE, K_q):
                sys.exit()
            if e.key == K_f or e.key == K_F11:
                toggle_fullscr()
            if e.key == K_UP:
                input_up = True
            if e.key == K_DOWN:
                input_down = True
            if e.key == K_LEFT:
                input_left = True
            if e.key == K_RIGHT:
                input_right = True
            if e.key == K_SPACE:
                input_A = True
            if e.key == K_LALT:
                input_B = True
        if e.type == KEYUP:
            if e.key == K_UP:
                input_up = False
            if e.key == K_DOWN:
                input_down = False
            if e.key == K_LEFT:
                input_left = False
            if e.key == K_RIGHT:
                input_right = False
            if e.key == K_SPACE:
                input_A = False
            if e.key == K_LALT:
                input_B = False

def main():
    global framecount
    camera = Camera(level_width, level_height)

    tiles = pygame.sprite.Group()
    platform_x = 0
    platform_y = 0
    for level_x in level:
        for level_y in level_x:
            if level_y == '1':
                p = Platform(platform_x, platform_y)
                tiles.add(p)
            platform_x += tile_size
        platform_x = 0
        platform_y += tile_size

    player = Player(200, 200)
    entities = pygame.sprite.Group()
    entities.add(player)

    while True:
        get_input()

        player_landing = player.inair
        player_speed = player.vel_y
        player.update(tiles, level_width, level_height,
            input_down,
            input_left,
            input_up,
            input_right,
            input_A,
            input_B)
        camera.update(player)
        if player.inair and player.vel_y == 0:
            screenshake(-player_speed / 20, 0, 3)
        if player_landing and not player.inair:
            screenshake(player_speed / 20, 0, 3)

        screen.fill(bgcolor)
        i = 0
        for e in tiles:
            screen.blit(e.image, camera.apply(e))
            i += 1
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
        timer.tick(framerate)
        framecount += 1



class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill(platformcolor)
        self.rect = pygame.Rect(x, y, tile_size, tile_size)

class Camera(object):
    #camera is a rectangle describing the coordinates of the window within the world space
    def __init__(self, width, height):
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        result = target.rect.move(self.state.topleft)
        if (screenshake_frames > 0):
            shake = (screenshake_x, screenshake_y) if (framecount % 2 == 0) else (-screenshake_x, -screenshake_y)
            result = result.move(shake)
        return result

    def apply_parallax(self, target, offset_x, offset_y, parallax_x, parallax_y):
        return (pygame.Rect(
            target.rect.left + offset_x + self.state[0] * parallax_x,
            target.rect.top + offset_y + self.state[1] * parallax_y,
            self.state[2], self.state[3]))

    def update(self, target):
        self.state = self.playerCamera(self.state, target.rect)
        
    def playerCamera(self, level, target_rect):
        global screenshake_frames
        global screenshake_x
        global screenshake_y
        if (screenshake_frames > 0):
            screenshake_frames -= 1
            if (screenshake_frames < screenshake_x):
                screenshake_x -= 1
            if (screenshake_frames < screenshake_y):
                screenshake_y -= 1
        xcoord = target_rect[0]
        ycoord = target_rect[1]
        xlength = level[2]
        ylength = level[3]
        xcoord = -xcoord + (win_width/2)
        ycoord = -ycoord + (win_height/2)
        if xcoord > -16:
            xcoord = -16
        if xcoord < -(level.width-win_width)+16:
            xcoord = -(level.width-win_width)+16
        if ycoord > 0:
            ycoord = 0
        if ycoord < -(level.height-win_height):
            ycoord = -(level.height-win_height)
        return pygame.Rect(xcoord, ycoord, xlength, ylength)



if(__name__ == "__main__"):
    main()
