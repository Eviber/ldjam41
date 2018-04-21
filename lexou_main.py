import sys, pygame
from pygame import *

import spritesheet
import player
import pyganim



class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.Surface((16, 16))
        self.image.fill(0xFFFFFF)
        self.rect = pygame.Rect(x, y, 16, 16)

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
        xcoord = -xcoord + (windowWidth/2)
        ycoord = -ycoord + (windowHeight/2)
        if xcoord > -16:
            xcoord = -16
        if xcoord < -(level.width-windowWidth)+16:
            xcoord = -(level.width-windowWidth)+16
        if ycoord > 0:
            ycoord = 0
        if ycoord < -(level.height-windowHeight):
            ycoord = -(level.height-windowHeight)
        return pygame.Rect(xcoord, ycoord, xlength, ylength)

framerate = 5
timer = pygame.time.Clock()

size = (width, height) = (256, 224)

levelSize = (levelWidth, levelHeight) = (512, 224)
level = [
"P                              P",
"P                              P",
"P                              P",
"P                              P",
"P                              P",
"P                              P",
"P                              P",
"P                              P",
"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
"P                              P",
"P                              P",
"P                              P",
"P                              P"]

input_down  = False
input_left  = False
input_up    = False
input_right = False
input_A     = False
input_B     = False

def get_input():
    input_down  = False
    input_left  = False
    input_up    = False
    input_right = False
    input_A     = False
    input_B     = False
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == KEYDOWN:
            if e.key in (K_ESCAPE, K_q):
                sys.exit()
            if e.key == K_UP:    input_up = True
            if e.key == K_DOWN:  input_down = True
            if e.key == K_LEFT:  input_left = True
            if e.key == K_RIGHT: input_right = True
            if e.key == K_SPACE: input_A = True
            if e.key == K_LALT:  input_B = True

def main():
    pygame.init()
    screen = pygame.display.set_mode(size, 0, 16)
    pygame.display.set_caption("Golf Rush")

    camera = Camera(levelWidth, levelHeight)

    platforms = pygame.sprite.Group()
    platform_x = 0
    platform_y = 0
    for level_x in level:
        for level_y in level_x:
            if level_y == "P":
                p = Platform(platform_x, platform_y)
                platforms.add(p)
            platform_x += 16
        platform_x = 0
        platform_y += 16

    player = Player(16, 128)
    entities.add(player)
    entities = pygame.sprite.Group()
    #entities.add(player sprite ?)

    while True:
        get_input()

        #player.update()
        #camera.update(player)

        for e in platforms:
            screen.blit(e.image, camera.apply(e))
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
        timer.tick(framerate)

if(__name__ == "__main__"):
    main()