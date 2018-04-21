import sys, pygame
from pygame import *

import spritesheet



class Camera(object):
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

framerate = 60

input_down  = False
input_left  = False
input_up    = False
input_right = False
input_A     = False
input_B     = False

size = (width, height) = (256, 224)

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

done = False

def main():
    pygame.init()
    screen = pygame.display.set_mode(size, 0, 16)
    pygame.display.set_caption("Golf Rush")

    camera = Camera(levelWidth, levelHeight)

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

    while not done:
    # main game loop
        timer.tick(framerate)

        camera.update(player)

        get_input()

        #player.update()

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

    raise SystemExit("QUIT")

def get_input():
    input_down  = False
    input_left  = False
    input_up    = False
    input_right = False
    input_A     = False
    input_B     = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            done = True
        if e.type == KEYDOWN and e.key == K_UP:
            input_up = True
        if e.type == KEYDOWN and e.key == K_DOWN:
            input_down = True
        if e.type == KEYDOWN and e.key == K_LEFT:
            input_left = True
        if e.type == KEYDOWN and e.key == K_RIGHT:
            input_right = True
        if e.type == KEYDOWN and e.key == K_SPACE:
            input_A = True
        if e.type == KEYDOWN and e.key == K_LALT:
            input_B = True

if(__name__ == "__main__"):
    main()