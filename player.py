from balls import *
import pyganim
import spritesheet

framerate = 1 / (1000/60)

alpha = (211, 249, 188) # 0xD3F9BC

sheet = spritesheet.spritesheet("tiger.png")
anim_idle = sheet.image_at((  1,  1,64,64), alpha)
anim_walk = pyganim.PygAnimation([
            (sheet.image_at((  1, 66, 64, 64), alpha), 0.1),
            (sheet.image_at(( 66, 66, 64, 64), alpha), 0.1),
            (sheet.image_at((131, 66, 64, 64), alpha), 0.1),
            (sheet.image_at((196, 66, 64, 64), alpha), 0.1),
            (sheet.image_at((261, 66, 64, 64), alpha), 0.1),
            (sheet.image_at((326, 66, 64, 64), alpha), 0.1)])
anim_jumpcharge = [sheet.image_at((  1, 131, 64, 64), alpha),
            sheet.image_at(( 66, 131, 64, 64), alpha),
            sheet.image_at((131, 131, 64, 64), alpha)]
anim_jump = sheet.image_at((261,131,64,64), alpha)
anim_fall = sheet.image_at((326,131,64,64), alpha)
anim_golfcharge = pyganim.PygAnimation([
            (sheet.image_at((  1, 196, 64, 64), alpha), 0.2),
            (sheet.image_at(( 66, 196, 64, 64), alpha), 0.2),
            (sheet.image_at((131, 196, 64, 64), alpha), 0.2),
            (sheet.image_at((196, 196, 64, 64), alpha), 0.2),
            (sheet.image_at((261, 196, 64, 64), alpha), 0.2),
            (sheet.image_at((326, 196, 64, 64), alpha), 0.2)])
anim_golf = pyganim.PygAnimation([
            (sheet.image_at(( 1, 261, 64, 64), alpha), 0.1),
            (sheet.image_at((66, 261, 64, 64), alpha), 0.1)])

sfx_jump = pygame.mixer.Sound("sfx_jump.wav")

from enum import Enum
class PlayerStatus(Enum):
	idle		= 0
	walk		= 1
	jumpcharge	= 2
	jump		= 3
	golfcharge	= 4
	golf		= 5
	damage		= 6

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = anim_idle
        self.rect = pygame.Rect(x, y, 64, 64)
        self.hitbox = pygame.Rect(0, 0, 32, 48)
        self.hitbox.midbottom = self.rect.midbottom
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.maxvel_x = 35
        self.maxvel_y = 500

        self.status = PlayerStatus.idle

        self.flip = False
        self.inair = True
        self.jumpcharge = 0
        self.golfcharge = 0
        self.maxgolf = 70

        self.allow_golf = True



    def update(self, tiles, level_width, level_height,
        input_down,
        input_left,
        input_up,
        input_right,
        input_A,
        input_B):

        if self.status == PlayerStatus.damage:
            pass
        if self.status == PlayerStatus.jumpcharge:
            self.jump(input_A)
        elif self.status == PlayerStatus.golfcharge:
            self.golf(input_B)
        elif input_A:
        	self.jump(input_A)
        elif input_B:
        	self.golf(input_B)
        elif input_left or input_right:
            self.walk(input_left, input_right)
        else:
            self.idle()

        

        if self.inair:
            self.fall()

        self.update_rect(tiles, level_width, level_height)

        if isinstance(self.image, pyganim.PygAnimation):
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
        floor = pygame.Rect(self.hitbox.left, self.hitbox.bottom, self.hitbox.width, 1)
        floor_collide = False
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if vel_x > 0:
                    self.hitbox.right = tile.rect.left
                if vel_x < 0:
                    self.hitbox.left = tile.rect.right
                if vel_y > 0:
                    self.vel_y = 0
                    self.hitbox.bottom = tile.rect.top
                    self.status = PlayerStatus.idle
                    self.inair = False
                if vel_y < 0:
                    self.vel_y = 0
                    self.hitbox.top = tile.rect.bottom
            if (tile.rect.colliderect(floor)):
                floor_collide = True
        if not floor_collide:
            self.inair = True
        self.rect.midbottom = self.hitbox.midbottom



    def idle(self):
        self.status = PlayerStatus.idle
        self.vel_x = 0
        self.image = anim_idle

    def walk(self, input_left, input_right):
        if input_left and input_right:
            self.flip = False
            self.vel_x = 0
        else:
            self.vel_x = self.maxvel_x if (input_right) else -self.maxvel_x
            self.flip = input_left
            if not self.inair:
                self.status = PlayerStatus.walk
                self.image = anim_walk
                anim_walk.play()

    def fall(self):
        self.vel_y += 12
        if self.vel_y <= 0:
            self.image = anim_jump
        else:
            self.image = anim_fall

    def jump(self, input_A):
        if not self.inair:
            if input_A:
                if self.status != PlayerStatus.jumpcharge:
                    self.status = PlayerStatus.jumpcharge
                    self.jumpcharge = 30
                self.vel_x = 0
                self.jumpcharge += 10
                if self.jumpcharge < self.maxvel_y:
                    self.image = anim_jumpcharge[round(self.jumpcharge / self.maxvel_y * 2)]
                else:
                    self.jumpcharge = self.maxvel_y
            elif self.jumpcharge > 0:
                self.status = PlayerStatus.jump
                self.vel_y = -self.jumpcharge
                self.jumpcharge = 0
                self.inair = True

    def golf(self, input_B):
        if input_B:
            self.status = PlayerStatus.golfcharge
            self.vel_x = 0
            self.golfcharge += 1
            if self.golfcharge < self.maxgolf:
                self.image = anim_golfcharge
                anim_golfcharge.play()
            else:
                self.golfcharge = self.maxgolf
                anim_golfcharge.stop()
        elif self.golfcharge > 0:
            self.status = PlayerStatus.golf
            self.allow_golf = False
            #ball.vel_y = -(self.golfcharge * 10)
            self.golfcharge = 0
        else:
            self.allow_golf = True
