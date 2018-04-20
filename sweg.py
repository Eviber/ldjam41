import sys, pygame

pygame.init()


size = (width, height) = (1000, 240)
black = (0, 0, 0)

screen = pygame.display.set_mode(size, pygame.RESIZABLE)

sweg = pygame.image.load("sweg.png")

sprites = [	sweg.get_rect(),
			sweg.get_rect(),
			sweg.get_rect(),
			sweg.get_rect()]
speed = [	[1,3],
			[-1,2],
			[2,-1],
			[3,1]]

lastticks = pygame.time.get_ticks()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	for i in range(0, 4):
		sprites[i] = sprites[i].move(speed[i])
		if sprites[i].left < 0 or sprites[i].right > width:
			speed[i][0] = -speed[i][0]
		if sprites[i].top < 0 or sprites[i].bottom > height:
			speed[i][1] = -speed[i][1]
	
	screen.fill(black)
	for i in range(0, 4):
		screen.blit(sweg, sprites[i])
	pygame.display.flip()
	while lastticks + 1000 / 60 > pygame.time.get_ticks():
		pass
	lastticks = pygame.time.get_ticks()
