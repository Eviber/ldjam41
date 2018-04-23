import pygame, pyganim, spritesheet, config
from entity import *
from balls import *
from enum import Enum

anim_idle = Gl.sheet_tiger.image_at((  1,  1,64,64), Gl.alpha)
anim_walk = pyganim.PygAnimation([
        (Gl.sheet_tiger.image_at((  1, 66, 64, 64), Gl.alpha), 0.1),
        (Gl.sheet_tiger.image_at(( 66, 66, 64, 64), Gl.alpha), 0.1),
        (Gl.sheet_tiger.image_at((131, 66, 64, 64), Gl.alpha), 0.1),
        (Gl.sheet_tiger.image_at((196, 66, 64, 64), Gl.alpha), 0.1),
        (Gl.sheet_tiger.image_at((261, 66, 64, 64), Gl.alpha), 0.1),
        (Gl.sheet_tiger.image_at((326, 66, 64, 64), Gl.alpha), 0.1)])
anim_jumpcharge = [Gl.sheet_tiger.image_at((  1, 131, 64, 64), Gl.alpha),
            Gl.sheet_tiger.image_at(( 66, 131, 64, 64), Gl.alpha),
            Gl.sheet_tiger.image_at((131, 131, 64, 64), Gl.alpha)]
anim_jump = Gl.sheet_tiger.image_at((261,131,64,64), Gl.alpha)
anim_fall = Gl.sheet_tiger.image_at((326,131,64,64), Gl.alpha)
anim_golfcharge = [Gl.sheet_tiger.image_at((  1, 196, 64, 64), Gl.alpha),
            Gl.sheet_tiger.image_at(( 66, 196, 64, 64), Gl.alpha),
            Gl.sheet_tiger.image_at((131, 196, 64, 64), Gl.alpha),
            Gl.sheet_tiger.image_at((196, 196, 64, 64), Gl.alpha),
            Gl.sheet_tiger.image_at((261, 196, 64, 64), Gl.alpha),
            Gl.sheet_tiger.image_at((326, 196, 64, 64), Gl.alpha)]
anim_golf = [Gl.sheet_tiger.image_at((  1, 261, 64, 64), Gl.alpha),
             Gl.sheet_tiger.image_at(( 66, 261, 64, 64), Gl.alpha),
             Gl.sheet_tiger.image_at((131, 261, 64, 64), Gl.alpha)]

class PlayerStatus(Enum):
    damage     = 0
    idle       = 1
    walk       = 2
    jumpcharge = 3
    jump       = 4
    golfcharge = 5
    golf       = 6
    slide      = 7

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, anim_idle, x, y)
        self.hitbox = pygame.Rect(0, 0, 32, 48)
        self.hitbox.midbottom = self.rect.midbottom
        self.maxvel_x = 35
        self.maxvel_y = 500

        self.status = PlayerStatus.idle

        self.jumpcharge = 0
        self.golfcharge = 0
        self.golfanim   = 0
        self.maxgolf    = 1000


    def update(self):

        if self.status == PlayerStatus.damage:
            pass
        elif self.status == PlayerStatus.jumpcharge:
            self.jump()
        elif self.status == PlayerStatus.golfcharge or self.status == PlayerStatus.golf:
            self.golf()
        elif self.status == PlayerStatus.slide:
            self.slide()
        elif Gl.input_A:
            self.jump()
        elif Gl.input_B:
            self.golf()
        elif Gl.input_left or Gl.input_right:
            self.walk()
        else:
            self.idle()

        if self.inair:
            self.fall()

        self.update_rect()
        self.rect.midbottom = self.hitbox.midbottom

        if self.status == PlayerStatus.golf:
            for row in range(int(self.hitbox.x / Gl.tile_size) - (self.flip == True), int((self.hitbox.x + self.hitbox.w) / Gl.tile_size) + (self.flip == False)):
                for col in range(int(self.hitbox.y / Gl.tile_size), int((self.hitbox.y + self.hitbox.h) / Gl.tile_size)):
                    Gl.tiles[col][row] = None

        if isinstance(self.image, pyganim.PygAnimation):
            self.image = self.image.getCurrentFrame()
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def idle(self):
        self.status = PlayerStatus.idle
        self.vel_x = 0
        self.image = anim_idle

    def walk(self):
        if Gl.input_left and Gl.input_right:
            self.flip = False
            self.vel_x = 0
        else:
            self.vel_x = self.maxvel_x if Gl.input_right else -self.maxvel_x
            self.flip = Gl.input_left
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

    def jump(self):
        if not self.inair:
            if Gl.input_A:
                if self.status != PlayerStatus.jumpcharge:
                    self.status = PlayerStatus.jumpcharge
                    self.jumpcharge = 100
                self.vel_x = 0
                self.jumpcharge += 10
                if self.jumpcharge > self.maxvel_y:
                    self.jumpcharge = self.maxvel_y
                self.image = anim_jumpcharge[int(self.jumpcharge / self.maxvel_y * 2)]
            else:
                self.status = PlayerStatus.jump
                self.vel_y = -self.jumpcharge
                self.jumpcharge = 0

    def golf(self):
        if Gl.input_B and self.status != PlayerStatus.golf:
            self.status = PlayerStatus.golfcharge
            self.vel_x = 0
            self.golfcharge += 3
            print(self.golfcharge)
            if self.golfcharge > self.maxgolf:
                self.golfcharge = self.maxgolf
            self.image = anim_golfcharge[int(self.golfcharge / self.maxgolf * 5)]
        elif self.status == PlayerStatus.golfcharge or (self.golfanim < 20 and self.status == PlayerStatus.golf):
            #apply swing
            self.status = PlayerStatus.golf
            if self.golfanim < 3:
                self.image = anim_golf[0]
            elif self.golfanim < 6:
                self.image = anim_golf[1]
            else:
                self.image = anim_golf[2]
            self.golfanim += 1
        else:
            self.golfanim = 0
            self.golfcharge = 0
            self.status = PlayerStatus.idle

    def slide(self):
        pass
