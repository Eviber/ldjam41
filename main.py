import sys, pygame
from pygame import *
from player import *

size = (win_width, win_height) = (256, 224)

bgcolor = (69, 69, 69)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Golf Rush")
framerate = 60
timer = pygame.time.Clock()

tile_size = 16
level_size = (level_width, level_height) = (32 * tile_size, 16 * tile_size)
level = [
"P                              P",
"P                              P",
"P                            PPP",
"P                              P",
"P                              P",
"P                         P    P",
"P      P                  P    P",
"P     PPP           PP    P    P",
"PPPPPPPPPPPPPPPPPPPPPPPPPPPPP  P",
"PPPPPPPPPPPPPPPPPPPPPPPPPPPPP  P",
"P                     P        P",
"P                P             P",
"P          P                   P",
"P                              P",
"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]

input_down  = False
input_left  = False
input_up    = False
input_right = False
input_A     = False
input_B     = False


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
    camera = Camera(level_width, level_height)

    tiles = pygame.sprite.Group()
    platform_x = 0
    platform_y = 0
    for level_x in level:
        for level_y in level_x:
            if level_y == 'P':
                p = Platform(platform_x, platform_y)
                tiles.add(p)
            platform_x += tile_size
        platform_x = 0
        platform_y += tile_size

    player = Player(20, 20)
    entities = pygame.sprite.Group()
    entities.add(player)

    while True:
        get_input()

        player.update(tiles, level_width, level_height,
            input_down,
            input_left,
            input_up,
            input_right,
            input_A,
            input_B)
        camera.update(player)

        screen.fill(bgcolor)
        for e in tiles:
            screen.blit(e.image, camera.apply(e))
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
        timer.tick(framerate)



class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill(0xFFFFFF)
        self.rect = pygame.Rect(x, y, tile_size, tile_size)

class Camera(object):
    #camera is a rectangle describing the coordinates of the window within the world space
    def __init__(self, width, height):
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.playerCamera(self.state, target.rect)
        
    def playerCamera(self, level, target_rect):
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