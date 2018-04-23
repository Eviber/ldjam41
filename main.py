import sys, pygame, spritesheet, config
from config import *
from player import *

def render(camera, entities):
    Gl.screen.fill(Gl.bgcolor)
    Gl.screen.blit(Gl.bg, camera.apply_parallax(0, 0, 0.2, 0.2))
    for row in Gl.tiles:
        for tile in row:
            rect = camera.apply(tile.rect)
            if (rect.colliderect(Gl.screen_rect)):
                Gl.screen.blit(tile.image, rect)
    for e in entities:
        rect = camera.apply(e.rect)
        if (rect.colliderect(Gl.screen_rect)):
            Gl.screen.blit(e.image, rect)

#sheet_fx = spritesheet.spritesheet("fx.png")
#fx_explosion_ground_big = [(sheet_fx.image_at((1 + x,   1,  85,  54), alpha), 0.1) for x in range(0, 11,  86)]
#fx_explosion_normal_big = [(sheet_fx.image_at((1 + x,  58, 100,  84), alpha), 0.1) for x in range(0,  8, 101)]
#fx_explosion_aerial_big = [(sheet_fx.image_at((1 + x, 145, 100, 100), alpha), 0.1) for x in range(0,  8, 101)]
#fx_explosion_ground = [(sheet_fx.image_at((1 + x, 248, 52,  33), alpha), 0.1) for x in range(0, 11, 86)]
#fx_explosion_normal = [(sheet_fx.image_at((1 + x, 284, 63,  84), alpha), 0.1) for x in range(0,  8, 64)]
#fx_explosion_aerial = [(sheet_fx.image_at((1 + x, 340, 70, 100), alpha), 0.1) for x in range(0,  8, 71)]
#fx_dust_large = [(sheet_fx.image_at((1 + x, 413, 26, 25), alpha), 0.1) for x in range(0,  6, 26)]
#fx_dust_small = [(sheet_fx.image_at((1 + x, 441, 19, 11), alpha), 0.1) for x in range(0,  6, 20)]

def main():
    camera = Camera(Gl.level_width * Gl.tile_size, Gl.level_height * Gl.tile_size)

    player = Player(300, 300)
    entities = pygame.sprite.Group()
    entities.add(player)

    ball = Ball(Gl.ball_golf, 16, 320, 250, player)
    entities.add(ball)

    while True:
        Gl.get_input()

        player_status = player.status
        player_landing = player.inair
        player_speed = player.vel_y
        player.update()
        camera.update(player)
        if player.inair and player.vel_y == 0:
            Gl.screenshake(-player_speed / 50, 0, 3)
        if player_landing and not player.inair:
            Gl.screenshake(player_speed / 30, 0, 3)
        if player_status == PlayerStatus.golfcharge and player.status == PlayerStatus.golf:
            for e in entities:
                if isinstance(e, Ball) and e.rect.colliderect(player.rect):
                    e.hit(player.golfcharge, player.golfcharge)

        for e in entities:
            if isinstance(e, Ball):
                ball.update()
            elif not isinstance(e, Player):
                e.update();
        render(camera, entities)
        pygame.display.update()

        Gl.timer.tick(Gl.framerate)
        Gl.framecount += 1

class Camera(object):
    #camera is a rectangle describing the coordinates of the window within the world space
    def __init__(self, width, height):
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        result = target.move(self.state.topleft)
        if (Gl.screenshake_frames > 0):
            shake = (Gl.screenshake_x, Gl.screenshake_y) if (Gl.framecount % 4 < 2) else (-Gl.screenshake_x, -Gl.screenshake_y)
            result = result.move(shake)
        return result

    def apply_parallax(self, offset_x, offset_y, parallax_x, parallax_y):
        return (pygame.Rect(
            offset_x + self.state[0] * parallax_x,
            offset_y + self.state[1] * parallax_y,
            self.state[2], self.state[3]))

    def update(self, target):
        self.state = self.playerCamera(self.state, target.rect)

    def playerCamera(self, level, target_rect):
        if (Gl.screenshake_frames > 0):
            Gl.screenshake_frames -= 1
            if (Gl.screenshake_frames < Gl.screenshake_x):
                Gl.screenshake_x -= 1
            if (Gl.screenshake_frames < Gl.screenshake_y):
                Gl.screenshake_y -= 1
        xcoord = target_rect[0]
        ycoord = target_rect[1]
        xlength = level[2]
        ylength = level[3]
        xcoord = -xcoord + (Gl.win_width/2)
        ycoord = -ycoord + (Gl.win_height/2)
        if xcoord > -16:
            xcoord = -16
        if xcoord < -(level.width-Gl.win_width)+16:
            xcoord = -(level.width-Gl.win_width)+16
        if ycoord > 0:
            ycoord = 0
        if ycoord < -(level.height-Gl.win_height):
            ycoord = -(level.height-Gl.win_height)
        return pygame.Rect(xcoord, ycoord, xlength, ylength)

if(__name__ == "__main__"):
    main()
