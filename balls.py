import pygame
from entity import *

class Ball(Entity):
    def __init__(self, image, size, x, y):
        Entity.__init__(self, image, size, x, y)
        self.size = self.image.get_width
        self.maxvel_x = 0
        self.maxvel_y = 0
        self.ang_mmt = 0 #positive is clockwise
        #self.rotations = self.build_rotations #wtf dude
        self.cur_orient = 0

        self.hasMomentum = False
        self.isRolling = False
        self.exploding = False

    def build_rotations(self):
        img = self.image
        rots = self.size
        incr = 360 / rots;
        res = []
        res.append(img)
        for i in range(1, rots):
            res.append(transform.rotate(img, i * incr))
        return res

    def fall(self):
        self.vel_y += 12
        if self.vel_x < 0:
            self.vel_x += 1
        if self.vel_x > 0:
            self.vel_x -= 1

    def hit(self, xvel, yvel):
        self.vel_x += xvel
        self.vel_y += yvel

    def update(self):
        if (self.inair):
            self.fall()
        else:
            self.idle()
        self.update_rect(tiles, level_width, level_height)

class Bomb(Ball):
    def __init__(self, x, y):
        Ball.__init__(self, img_bomb, 16, x, y)
        self.exploding = True

class Pebble(Ball):
    def __init__(self, x, y):
        Ball.__init__(self, img_pebble, 8, x, y)
