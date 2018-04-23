import sys, pygame, spritesheet, config
from player import *
from balls import *



def render(entities):
    Gl.screen.fill(Gl.bgcolor)
    Gl.screen.blit(Gl.bg, Gl.camera.apply_parallax(0, 0, 0.2, 0.2))
    for row in range(-int(Gl.camera.state.x / Gl.tile_size), -int((Gl.camera.state.x - Gl.win_width) / Gl.tile_size) + 1):
        for col in range(-int(Gl.camera.state.y / Gl.tile_size), -int((Gl.camera.state.y - Gl.win_height) / Gl.tile_size) + 1):
            if Gl.tiles[col][row] != None:
                Gl.screen.blit(Gl.tiles[col][row].image, Gl.camera.apply(Gl.tiles[col][row].rect))
    for e in entities:
        rect = Gl.camera.apply(e.rect)
        if (rect.colliderect(Gl.screen_rect)):
            Gl.screen.blit(e.image, rect)
        if e.fx and e.fx.rect and e.fx.image:
            rect = Gl.camera.apply(e.fx.rect)
            if (rect.colliderect(Gl.screen_rect)):
                Gl.screen.blit(e.fx.image, rect)



def update_entities(player, entities):
    player_status = player.status
    player_inair = player.inair
    player_speed = player.vel_y

    for e in entities:
        e.update()
        if e.fx:
            e.fx.update()

    if player.vel_y < 0 and not player_inair and player.inair: # player jump
        Gl.camera.screenshake(player.vel_y / 50, 0, 2)
        player.fx.play(Gl.fx_dust_large, player.rect.x, player.rect.y)
    if player.vel_y == 0 and player.inair: # player hit ceiling
        Gl.camera.screenshake(-player_speed / 50, 0, 3)
    if player_inair and not player.inair: # player landing
        Gl.camera.screenshake(player_speed / 30, 0, 3)
        Gl.sfx_land.set_volume(player_speed / player.maxvel_y)
        Gl.sfx_land.play()
    if player_status == PlayerStatus.golfcharge and player.status == PlayerStatus.golf:
        Gl.sfx_golf_swing.play()
        for e in entities:
            if isinstance(e, Ball) and e.rect.colliderect(player.rect):
                e.hit(player.golfcharge, player.golfcharge)
                Gl.sfx_golf_hit.play()



def main():
    entities = pygame.sprite.Group()

    player = Player(300, 300)
    entities.add(player)

    entities.add(Ball(Gl.ball_golf, 16, 320, 250, player))
    entities.add(Ball(Gl.ball_poke, 16, 350, 250, player))

    while True:
        Gl.get_input()

        update_entities(player, entities)

        Gl.camera.update(player)
        render(entities)
        pygame.display.update()

        Gl.timer.tick(Gl.framerate)
        Gl.framecount += 1



if(__name__ == "__main__"):
    main()
