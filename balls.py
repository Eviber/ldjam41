import pygame
from pygame import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.size = self.image.get_width
        self.pos_x = x
        self.pos_y = y
        self.vel_x = 0
        self.vel_y = 0
        self.rotations = self.build_rotations
        #index 0 is the default sprite orientation

        self.onGround = False
        self.hasMomentum = False
        self.isRolling

    def build_rotations(self):
        img = self.image
        rots = self.size
        incr = 360 / rots;
        res = []
        res.append(img)
        for i in range(1, rots):
            res.append(transform.rotate(img, i * incr))
        return res

    def update(self):
        vel_x = self.vel_x
        vel_y = self.vel_y

        #collision
        #onground

        quadnorm = vel_x * vel_x + vel_y * vel_y
        self.hasMomentum = quadnorm > 10
        self.isRolling = quadnorm > 0 and not self.hasMomentum and self.onGround


class Bomb(Ball):
    def __init__(self):
        Ball.__init__(self)



"""
screen_width = 1280
screen_height = 720

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))

BLACK = (0,0,0)

ballImg = pygame.image.load("ball.jpg")
ballPosition = [0,0]
speed = 1


def game_loop():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        #get all the keys being pressed
        keys = pygame.key.get_pressed()


        #depending on what key the user presses, update ball x and y position accordingly
        if keys[pygame.K_UP]:
            ballPosition[1] -= speed
        if keys[pygame.K_DOWN]:
            ballPosition[1] += speed
        if keys[pygame.K_LEFT]:
            ballPosition[0] -= speed
        if keys[pygame.K_RIGHT]:
            ballPosition[0] += speed


        screen.fill(BLACK) #fill the screen with black
        screen.blit(ballImg, ballPosition) #draw the ball
        pygame.display.update() #update the screen

game_loop()"""