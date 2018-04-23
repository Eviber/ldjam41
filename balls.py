from entity import *

class Ball(Entity):
    def __init__(self, image, size, x, y, player):
        Entity.__init__(self, image, x, y)
        self.size = self.image.get_width
        self.maxvel_x = 200
        self.maxvel_y = 200
        self.ang_mmt = 0 #positive is clockwise
        #self.rotations = self.build_rotations #wtf dude
        self.cur_orient = 0
        self.player = player

        self.bounce_x = 0.6
        self.bounce_y = 0.7
        self.isrolling = False

    def build_rotations(self):
        img = self.image
        rots = self.size
        incr = 360 / rots
        res = []
        res.append(img)
        for i in range(1, rots):
            res.append(pygame.transform.rotate(img, i * incr))
        return res

    def update_momentum(self):
        self.hasMomentum = self.vel_x * self.vel_x + self.vel_y * self.vel_y > 10

    def fall(self):
        self.vel_y += 12
        if self.vel_x < 0:
            self.vel_x += 1
        if self.vel_x > 0:
            self.vel_x -= 1

    def hit(self, xvel, yvel):
        self.vel_x += xvel if not self.player.flip else -xvel
        print(self.player.flip, xvel, self.vel_x)
        self.vel_y -= yvel

    def update(self):
        #TODO global tiles
        self.update_momentum()
        if self.inair:
            self.fall()
        else:
            self.idle()

        self.update_rect()
        self.rect.center = self.hitbox.center



class Bomb(Ball):
    def __init__(self, x, y):
        global img_bomb
        Ball.__init__(self, img_bomb, 16, x, y)
        self.exploding = False



class Pebble(Ball):
    def __init__(self, x, y):
        global img_pebble
        Ball.__init__(self, img_pebble, 8, x, y)
