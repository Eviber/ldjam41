from entity import *

class Ball(Entity):
    def __init__(self, image, size, x, y, player):
        Entity.__init__(self, image, x, y)
        self.size = size #serves as mass
        self.maxvel_x = 600
        self.maxvel_y = 600
        self.ang_mmt = 0            #positive is clockwise
        #self.rotations = self.build_rotations
        self.cur_orient = 0
        self.player = player
        self.fall_speed = size * 2  #acceleration due to gravity

        self.bounce_sfx = Gl.sfx_ball_bounce
        self.bounce = 0.5           #impact dampening coef
        self.friction = 0.3         #ground friction dampening coef
        self.isrolling = False
        self.hasMomentum = False

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
        self.hasMomentum = (self.vel_x * self.vel_x + self.vel_y * self.vel_y > 1100)

    def fall(self):
        self.vel_y = self.vel_y + self.fall_speed
        self.vel_x = 0.995 * self.vel_x


    def roll(self):
        self.vel_x = self.friction * self.vel_x

    def hit(self, xvel, yvel):
        self.isrolling = False
        self.inair = True
        self.vel_x += xvel if not self.player.flip else -xvel
        print("face left : " if self.player.flip else "face right :", xvel, self.vel_x)
        self.vel_y -= yvel

    def update(self):
        self.update_momentum()
        if self.inair:
            self.fall()
        if self.isrolling:
            self.roll()
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
