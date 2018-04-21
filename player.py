import spritesheet
from pygame import *
from game import *

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface([40, 50])
        self.image.fill((110,100,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = 0
        self.yvel = 0
        self.inair = self.rect.bottom + 1 < win_height
        self.chargingjump = 0

    def update(self, screen, left, right, space):
        maxxvel = 100
        maxyvel = 800
        xvel = self.xvel
        yvel = self.yvel
        self.inair = self.rect.bottom + 1 < win_height
        if self.inair:
            yvel += 70
            if yvel > maxyvel:
                yvel = maxyvel
        if (left == True and xvel > 0) or (right == True and xvel < 0) or (left == right == False):
            xvel = 0
        if left:
#            xvel -= 2
#            if xvel > -20:
#                xvel = -20
#            if self.inair or xvel < -maxxvel:
                xvel = -maxxvel
        if right:
#            xvel += 2
#            if xvel < 20:
#                xvel = 20
#            if self.inair or xvel > maxxvel:
                xvel = maxxvel
        self.rect.h = 50
        if space and not self.inair:
            xvel = 0
            self.chargingjump += 500 / (1000/60)
            if self.chargingjump >= 400:
                self.rect.h = 50 - (32 * (self.chargingjump / 1500))
            if self.chargingjump > maxyvel:
                self.chargingjump = maxyvel
        if not space and self.chargingjump > 400:
            yvel = -self.chargingjump
            self.chargingjump = 0
        self.rect = self.rect.move([xvel / (1000/60), yvel / (1000/60)])
        if self.rect.bottom > win_height:
            self.rect.bottom = win_height
        screen.blit(self.image, self.rect)
        self.xvel = xvel
        self.yvel = yvel
