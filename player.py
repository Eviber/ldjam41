from balls import *
from pyganim import *

alpha = (211, 249, 188) # 0xD3F9BC

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = sheet.image_at((44,86,64,64), alpha)
        self.rect = pygame.Rect(x + 16, y + 16, 32, 48)
        self.pos_x = x
        self.pos_y = y
        self.vel_x = 0
        self.vel_y = 0

        self.takingDamage = False
        self.idling = True
        self.walking = False
        self.crouching = False
        self.jumping = False
        self.swinging = False
        self.jumpswinging = False

        self.allow_jump = True
        self.allow_swing = True

        self.inair = False
        self.chargingjump = 0

    def update(self,
        input_down,
        input_left,
        input_up,
        input_right,
        input_A,
        input_B):

        maxxvel = 100
        maxyvel = 800
        xvel = self.vel_x
        yvel = self.vel_y

        if self.inair:
            yvel += 70
            if yvel > maxyvel:
                yvel = maxyvel
        if (input_left and xvel > 0) or (input_right and xvel < 0) or (input_left == input_right == False):
            xvel = 0
        if input_left:
#            xvel -= 2
#            if xvel > -20:
#                xvel = -20
#            if self.inair or xvel < -maxxvel:
                xvel = -maxxvel
        if input_right:
#            xvel += 2
#            if xvel < 20:
#                xvel = 20
#            if self.inair or xvel > maxxvel:
                xvel = maxxvel
        framerate = 1 / (1000/60)
        if input_A and not self.inair:
            xvel = 0
            self.chargingjump += 500 * framerate
            if self.chargingjump > maxyvel:
                self.chargingjump = maxyvel
        if not input_A and self.chargingjump > 400:
            yvel = -self.chargingjump
            self.chargingjump = 0

        self.vel_x = xvel
        self.vel_y = yvel

        self.pos_x += xvel * framerate
        self.pos_y += yvel * framerate

        self.rect.x = self.pos_x + 16
        self.rect.y = self.pos_y + 16

    def check_collisions(self, tiles):
        onground = False
        for tile in tiles:
            if pygame.sprite.collide_rect(self, tile):
                if self.vel_x > 0:
                    self.vel_x = 0
                    self.rect.right = tile.rect.left
                if self.vel_x < 0:
                    self.vel_x = 0
                    self.rect.left = tile.rect.right
                if self.vel_y > 0:
                    self.vel_y = 0
                    self.rect.bottom = tile.rect.top
                    self.inair = False
                    self.jumping = False
                if self.vel_y < 0:
                    self.vel_y = 0
                    self.rect.top = tile.rect.bottom
            if tile.rect.collidepoint(self.rect.center[0], self.rect.bottom + 1):
                onground = True
        if not onground:
            self.inair = True