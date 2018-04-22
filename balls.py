import pygame
from main import get_input, input_down, input_left, input_up, input_right, input_A, input_B

class Ball(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.sheet
        self.size = self.image.get_width
        self.pos_x = x
        self.pos_y = y
        self.vel_x = 0
        self.vel_y = 0
        self.ang_mmt = 0 #positive is clockwise
        self.rotations = self.build_rotations
        self.cur_orient = 0

        self.onGround = False
        self.hasMomentum = False
        self.isRolling = False

    def build_rotations(self):
        img = self.image
        rots = self.size
        incr = 360 / rots;
        res = []
        res.append(img)
        for i in range(1, rots):
            res.append(transform.rotate(img, i * incr))
        return res

    def update(self):
        vel_x = self.vel_x
        vel_y = self.vel_y

        jumpspeed = 10
        speed = 2

        """input_down input_left input_up input_right input_A input_B"""
        if input_down:
            self.vel_y -= jumpspeed
        if input_up:
            self.pos_y += speed
        if input_left:
            self.pos_x -= speed
            if self.pos_x < 0:
                self.pos_x += 1280
        if input_right:
            self.pos_x += speed
            if self.pos_x > 1280:
                self.pos_x -= 1280

        #collision
        #onground

        quadnorm = vel_x * vel_x + vel_y * vel_y
        self.hasMomentum = quadnorm > 10
        self.isRolling = quadnorm > 0 and not self.hasMomentum and self.onGround


class Bomb(Ball):
    def __init__(self, x, y):
        Ball.__init__(self, x, y)

"""
import spritesheet

def game_loop(screen, ball):
    BLACK = (0,0,0)
    framerate = 5
    timer = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        #get all the keys being pressed
        get_input()
        ball.update()

        screen.fill(BLACK)
        screen.blit(ball.image, (ball.pos_x, ball.pos_y))
        pygame.display.update()
        timer.tick(framerate)


def main_ball():
    screen_width = 1280
    screen_height = 720

    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))

    transparency = (0, 128, 128)
    ballImg = spritesheet.spritesheet("ball.png")
    ball = Ball(ballImg, 0, 0)

    game_loop(screen, ball)

main_ball()
"""