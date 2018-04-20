import sys, pygame

pygame.init()


size = width, height = 1000, 240

speed = [2, 2]

black = 0, 0, 0


screen = pygame.display.set_mode(size, pygame.RESIZABLE)

ball = pygame.image.load("beaugosse.png")

ballrect = ball.get_rect()

lastticks = pygame.time.get_ticks()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed) 
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    while lastticks + 1000 / 60 > pygame.time.get_ticks():
        pass
    lastticks = pygame.time.get_ticks()
