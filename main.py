import sys, pygame, spritesheet, config
from config import *
from player import *
from camera import *

def render(camera, entities):
    Gl.screen.fill(Gl.bgcolor)
    Gl.screen.blit(Gl.bg, camera.apply_parallax(0, 0, 0.2, 0.2))
    for row in range(-int(camera.state.x / Gl.tile_size), -int((camera.state.x - Gl.win_width) / Gl.tile_size) + 1):
        for col in range(-int(camera.state.y / Gl.tile_size), -int((camera.state.y - Gl.win_height) / Gl.tile_size) + 1):
            if Gl.tiles[col][row] != None:
                rect = camera.apply(Gl.tiles[col][row].rect)
                if (rect.colliderect(Gl.screen_rect)):
                    Gl.screen.blit(Gl.tiles[col][row].image, rect)
                Gl.screen.blit(Gl.tiles[col][row].image, rect)
    for e in entities:
        rect = camera.apply(e.rect)
        if (rect.colliderect(Gl.screen_rect)):
            Gl.screen.blit(e.image, rect)

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

if(__name__ == "__main__"):
    main()
