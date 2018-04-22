from balls import *
from pyganim import *
import spritesheet

framerate = 1 / (1000/60)

alpha = (211, 249, 188) # 0xD3F9BC

sheet = spritesheet.spritesheet("tiger.png")
anim_idle = sheet.image_at((44,86,64,64), alpha)
anim_jump = sheet.image_at((44,216,64,64), alpha)
anim_walk = PygAnimation([
            (sheet.image_at(( 44, 151, 64, 64), alpha), 0.1),
            (sheet.image_at((109, 151, 64, 64), alpha), 0.1),
            (sheet.image_at((174, 151, 64, 64), alpha), 0.1),
            (sheet.image_at((239, 151, 64, 64), alpha), 0.1),
            (sheet.image_at((304, 151, 64, 64), alpha), 0.1),
            (sheet.image_at((369, 151, 64, 64), alpha), 0.1)])

from enum import Enum
class PlayerStatus(Enum):
	idle = 0
	walk = 1
	jumpcharge = 2
	jump = 3
	golfcharge = 4
	golf = 5
	damage = 6

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = anim_idle
        self.rect = pygame.Rect(x, y, 64, 64)
        self.hitbox = pygame.Rect(0, 0, 32, 48)
        self.hitbox.midbottom = self.rect.midbottom
        self.vel_x = 0
        self.vel_y = 0
        self.maxvel_x = 50
        self.maxvel_y = 800

        self.status = PlayerStatus.idle

        self.flip = False
        self.inair = True
        self.jumpcharge = 0



    def update(self, tiles, level_width, level_height,
        input_down,
        input_left,
        input_up,
        input_right,
        input_A,
        input_B):

        if self.status == PlayerStatus.damage:
            pass
        elif input_up or input_down or input_left or input_right or input_A or input_B:
            self.walk(input_left, input_right)
        else:
            self.idle()

        self.jump(input_A)
        if self.inair:
            self.fall()

        self.update_rect(tiles, level_width, level_height)

        if isinstance(self.image, PygAnimation):
            #self.elapsed = self.image.elapsed
            self.image = self.image.getCurrentFrame()
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)



    def update_rect(self, tiles, level_width, level_height):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > level_width:
            self.rect.right = level_width
        if self.rect.bottom > level_height:
            self.rect.bottom = level_height

        if abs(self.vel_x) > self.maxvel_x:
            self.vel_x = self.maxvel_x if self.maxvel_x > 0 else -self.maxvel_x
        if abs(self.vel_y) > self.maxvel_y:
            self.vel_y = self.maxvel_y if self.maxvel_y > 0 else -self.maxvel_y

        self.rect.x += self.vel_x * framerate
        self.hitbox.midbottom = self.rect.midbottom
        self.check_collisions(tiles, self.vel_x, 0)
        self.rect.y += self.vel_y * framerate
        self.hitbox.midbottom = self.rect.midbottom
        self.check_collisions(tiles, 0, self.vel_y)



    def check_collisions(self, tiles, vel_x, vel_y):
        floor_collide = False
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if vel_x > 0:
                    self.vel_x = 0
                    self.hitbox.right = tile.rect.left
                    self.rect.midbottom = self.hitbox.midbottom
                if vel_x < 0:
                    self.vel_x = 0
                    self.hitbox.left = tile.rect.right
                    self.rect.midbottom = self.hitbox.midbottom
                if vel_y > 0:
                    self.vel_y = 0
                    self.hitbox.bottom = tile.rect.top
                    self.rect.midbottom = self.hitbox.midbottom
                    self.status = PlayerStatus.idle
                    self.inair = False
                if vel_y < 0:
                    self.vel_y = 0
                    self.hitbox.top = tile.rect.bottom
                    self.rect.midbottom = self.hitbox.midbottom
            if (tile.rect.collidepoint(self.hitbox.left + 1, self.hitbox.bottom) or
                tile.rect.collidepoint(self.hitbox.right - 2, self.hitbox.bottom)):
                floor_collide = True
        if not floor_collide:
            self.inair = True



    def idle(self):
        self.status = PlayerStatus.idle
        self.vel_x = 0
        self.image = anim_idle

    def walk(self, input_left, input_right):
        if input_left and input_right:
            self.flip = False
            self.vel_x = 0
        elif input_right:
            self.vel_x = self.maxvel_x
            self.flip = False
            if not self.inair:
                self.status = PlayerStatus.walk
                self.image = anim_walk
                anim_walk.play()
        elif input_left:
            self.vel_x = -self.maxvel_x
            self.flip = True
            if not self.inair:
                self.status = PlayerStatus.walk
                self.image = anim_walk
                anim_walk.play()

    def fall(self):
        self.vel_y += 20
        self.image = anim_jump

    def jump(self, input_A):
        if not self.inair:
            if input_A:
                self.status = PlayerStatus.jumpcharge
                self.vel_x = 0
                self.jumpcharge += 10
                if self.jumpcharge > self.maxvel_y:
                    self.jumpcharge = self.maxvel_y
            elif self.jumpcharge >= 10:
                self.status = PlayerStatus.jump
                self.vel_y = -self.jumpcharge
                self.jumpcharge = 0
                self.inair = True