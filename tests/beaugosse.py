import sys, pygame
from pygame import QUIT, KEYDOWN, K_ESCAPE, K_q, K_LEFT, K_RIGHT
from random import randint

pygame.init()


width, height = 1000, 1000

speed = [0, 0]

fillcolor = 20, 20, 20

ball = pygame.image.load("beaugosse.png")

pygame.display.set_icon(ball)
pygame.display.set_caption("Beaugosse")
screen = pygame.display.set_mode((width, height))

ballrect = ball.get_rect()

ballrect.x = width / 2;
ballrect.y = height / 2;

lastticks = pygame.time.get_ticks()

while 1:
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type == KEYDOWN:
            if event.key in (K_ESCAPE, K_q): sys.exit()

    if speed[0] < 3 or speed[0] > -3:
        speed[0] += randint(-1, 1)
    else:
        speed[0] += 1 if speed <= -3 else -1

    if speed[1] < 3 or speed[1] > -3:
        speed[1] += randint(-1, 1)
    else:
        speed[1] += 1 if speed <= -3 else -1

    ballrect = ballrect.move(speed) 
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
        ballrect = ballrect.move(speed) 
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
        ballrect = ballrect.move(speed) 
    screen.fill(fillcolor)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    while lastticks + 1000 / 60 > pygame.time.get_ticks():
        pass
    lastticks = pygame.time.get_ticks()
