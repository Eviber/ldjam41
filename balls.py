from entity import *
from math import hypot

class Ball(Entity):
    def __init__(self, image, size, x, y, player, entities):
        Entity.__init__(self, image, x, y, entities)
        self.entities = entities
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
        self.can_explode = True

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

    def explode(self):
        pass

    def update(self):
        self.update_momentum()
        if self.inair:
            self.fall()
        if self.isrolling:
            self.roll()
        else:
            self.idle()
        collided = len(self.update_rect())
        if (self.can_explode and collided and self.vel_x * self.vel_x + self.vel_y * self.vel_y > 50000):
            self.explode()
        self.rect.center = self.hitbox.center



class Bomb(Ball):
    def __init__(self, x, y, player, entities):
        global img_bomb
        Ball.__init__(self, Gl.ball_bomb, 16, x, y, player, entities)
        self.can_explode = True
        self.xploradius = 100

    def explode(self):
        self.kill()
        for e in self.entities:
                if (isinstance(e, Bomb) and hypot(e.hitbox.center[0] - self.hitbox.center[0],
                          e.hitbox.center[1] - self.hitbox.center[1]) < self.xploradius):
                    e.explode()
        rows = range(int((self.hitbox.center[0] - self.xploradius) / Gl.tile_size), int((self.hitbox.center[0] + self.xploradius) / Gl.tile_size))
        cols = range(int((self.hitbox.center[1] - self.xploradius) / Gl.tile_size), int((self.hitbox.center[1] + self.xploradius) / Gl.tile_size))
        lvl_w = Gl.level_width / Gl.tile_size
        lvl_h = Gl.level_height / Gl.tile_size
        for row in rows:
            if row < 0 or row > lvl_h:
                break
            for col in cols:
                if col < 0 or col > lvl_w:
                    break
                if (Gl.tiles[col][row] and hypot(
                    Gl.tiles[col][row].rect.center[0] - self.hitbox.center[0],
                    Gl.tiles[col][row].rect.center[1] - self.hitbox.center[1]) < self.xploradius):
                    Gl.tiles[col][row] = None
                    Gl.sfx_explosion.play()
                    Gl.play_fx(Gl.fx_explosion_normal_big, row * Gl.tile_size - randint(32, 96), col * Gl.tile_size - randint(32, 96))



class Pebble(Ball):
    def __init__(self, x, y, player, entities):
        global img_pebble
        Ball.__init__(self, img_pebble, 8, x, y, player, entities)
