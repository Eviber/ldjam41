from entity import *
from balls import *
import pyganim
import spritesheet
from enum import Enum

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
anim_golfcharge = [sheet.image_at((  1, 196, 64, 64), alpha),
                   sheet.image_at(( 66, 196, 64, 64), alpha),
                   sheet.image_at((131, 196, 64, 64), alpha),
                   sheet.image_at((196, 196, 64, 64), alpha),
                   sheet.image_at((261, 196, 64, 64), alpha),
                   sheet.image_at((326, 196, 64, 64), alpha)]
anim_golf = [sheet.image_at(( 1, 261, 64, 64), alpha),
             sheet.image_at((66, 261, 64, 64), alpha)]

sfx_jump = pygame.mixer.Sound("sfx_jump.wav")

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
        Entity.__init__(self, anim_idle, 64, x, y)
        self.hitbox = pygame.Rect(0, 0, 32, 48)
        self.hitbox.midbottom = self.rect.midbottom
        self.maxvel_x = 35
        self.maxvel_y = 500

        self.status = PlayerStatus.idle

        self.jumpcharge = 0
        self.golfcharge = 0
        self.maxgolf = 70


    def update(self, tiles,
        input_down,
        input_left,
        input_up,
        input_right,
        input_A,
        input_B):

        if self.status == PlayerStatus.damage:
            pass
        elif self.status == PlayerStatus.jumpcharge:
            self.jump(input_A)
        elif self.status == PlayerStatus.golfcharge or self.status == PlayerStatus.golf:
            self.golf(input_B)
        elif self.status == PlayerStatus.slide:
            self.slide()
        elif input_A or input_down:
            self.jump(input_A)
        elif input_B:
            self.golf(input_B)
        elif input_left or input_right:
            self.walk(input_left, input_right)
        else:
            self.idle()

        if self.inair:
            self.fall()

        self.update_rect(tiles)

        if isinstance(self.image, pyganim.PygAnimation):
            #self.elapsed = self.image.elapsed
            self.image = self.image.getCurrentFrame()
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

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
                    self.jumpcharge = 100
                self.vel_x = 0
                self.jumpcharge += 5
                if self.jumpcharge > self.maxvel_y:
                    self.jumpcharge = self.maxvel_y
                self.image = anim_jumpcharge[int((self.jumpcharge) / self.maxvel_y * 2)]
            else:
                self.status = PlayerStatus.jump
                self.vel_y = -self.jumpcharge
                self.jumpcharge = 0

    def golf(self, input_B):
        if input_B:
            self.status = PlayerStatus.golfcharge
            self.vel_x = 0
            self.golfcharge += 1
            if self.golfcharge > self.maxgolf:
                self.golfcharge = self.maxgolf
            self.image = anim_golfcharge[int((self.golfcharge) / self.maxgolf * 5)]
        elif self.golfcharge > 0 or (self.golfcharge > -30 and self.status == PlayerStatus.golf):
            #apply swing
            if self.golfcharge > 0:
                self.golfcharge = -1
            elif self.golfcharge > -5:
                self.image = anim_golf[0]
            else:
                self.image = anim_golf[1]
            self.status = PlayerStatus.golf
            #ball.vel_y = -(self.golfcharge * 10)
            self.golfcharge -= 1
        else:
            self.golfcharge = 0
            self.status = PlayerStatus.idle

    def slide(self):
        pass
