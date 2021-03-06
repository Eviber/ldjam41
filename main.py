import sys, pygame, spritesheet, config
from player import *
from balls import *
import copy


def render(entities):
    Gl.screen.fill(Gl.bgcolor)
    Gl.screen.blit(Gl.bg, Gl.camera.apply_parallax(0, 0, 0.2, 0.2))
    rows = range(-int(Gl.camera.state.x / Gl.tile_size), -int((Gl.camera.state.x - Gl.win_width) / Gl.tile_size) + 1)
    cols = range(-int(Gl.camera.state.y / Gl.tile_size), -int((Gl.camera.state.y - Gl.win_height) / Gl.tile_size) + 1)
    lvl_w = Gl.level_width / Gl.tile_size
    lvl_h = Gl.level_height / Gl.tile_size
    for row in rows:
        if row < 0 or row >= lvl_w:
            break
        for col in cols:
            if col < 0 or col >= lvl_h:
                break
            if Gl.tiles[col][row] != None:
                Gl.screen.blit(Gl.tiles[col][row].image, Gl.camera.apply(Gl.tiles[col][row].rect))
    player = 0
    ball = 0
    for e in entities:
        if isinstance(e, Player):
            player = e
        elif isinstance(e, Ball) and e.can_explode == False:
            ball = e
        rect = Gl.camera.apply(e.rect)
        if (rect.colliderect(Gl.screen_rect)):
            Gl.screen.blit(e.image, rect)
        if e.fx and e.fx.playing:
            rect = Gl.camera.apply(e.fx.rect)
            if (rect.colliderect(Gl.screen_rect)):
                Gl.screen.blit(e.fx.image, rect)
    minimap_w_ball_n_player = copy.copy(Gl.minimap)
    playpos = int(player.rect.x / Gl.tile_size) + 1, int(player.rect.y / Gl.tile_size) + 1
    ballpos = int(ball.rect.x / Gl.tile_size), int(ball.rect.y / Gl.tile_size)
    for px in range(3):
        for py in range(3):
            minimap_w_ball_n_player.set_at((playpos[0] * 3 + px, playpos[1] * 3 + py), (255, 0, 0))
            minimap_w_ball_n_player.set_at((ballpos[0] * 3 + px, ballpos[1] * 3 + py), (0, 0, 255))
    minimap_w_ball_n_player.set_at((ballpos[0] * 3 + 1, ballpos[1] * 3 + 1), (255, 255, 255))
    Gl.screen.blit(minimap_w_ball_n_player, minimap_w_ball_n_player.get_rect().move(20, 20))




def update_entities(player, entities):
    player_status = player.status
    player_inair = player.inair
    player_speed = player.vel_y

    for e in entities:
        e.update()
        if e.fx:
            e.fx.update()

    if player.vel_y < 0 and not player_inair and player.inair: # player jump
        player.fx.play(Gl.fx_dust_large, player.rect.midbottom[0] - 10, player.rect.y + 60, player.flip)
        Gl.camera.screenshake(player.vel_y / 50, 0, 2)
    if player.vel_y == 0 and player.inair: # player hit ceiling
        Gl.camera.screenshake(-player_speed / 50, 0, 3)
    if player_inair and not player.inair: # player landing
        player.fx.play(Gl.fx_dust_double, player.rect.midbottom[0] - 27, player.rect.y + 54, player.flip)
        Gl.camera.screenshake(player_speed / 30, 0, 3)
        Gl.sfx_land.set_volume(player_speed / player.maxvel_y)
        Gl.sfx_land.play()
    if player_status == PlayerStatus.golfcharge and player.status == PlayerStatus.golf:
        player.fx.play(Gl.fx_dust_large, player.rect.x + (-10 if player.flip else 50), player.rect.y + 40, player.flip)
        Gl.sfx_golf_swing.play()
        for e in entities:
            if isinstance(e, Ball) and e.rect.colliderect(player.rect):
                e.hit(player.golfcharge, player.golfcharge)
                Gl.camera.screenshake(player.golfcharge / 50, 2, 0)
                Gl.sfx_golf_hit.play()
        for col in range(int(player.hitbox.x / Gl.tile_size) - (player.flip == True), int((player.hitbox.x + player.hitbox.w) / Gl.tile_size) + (player.flip == False)):
            for row in range(int(player.hitbox.y / Gl.tile_size), int((player.hitbox.y + player.hitbox.h) / Gl.tile_size)):
                if Gl.tiles[row][col]:
                    if player.golfcharge >= player.maxgolf - 100:
                        Gl.tiles[row][col] = None
                        Gl.sfx_explosion.play()
                        if Gl.tiles[row + 1][col] is None:
                            Gl.play_fx(Gl.fx_explosion_aerial_big, col * Gl.tile_size - 32, row * Gl.tile_size - 32, player.flip)
                        else:
                            Gl.play_fx(Gl.fx_explosion_ground_big, col * Gl.tile_size - 32, row * Gl.tile_size - 22, player.flip)
                    else:
                        Gl.sfx_golf_hit.play()


def show(image):
    Gl.screen.blit(image, image.get_rect())
    pygame.display.update()

def main():
    show(Gl.img_tutorial)
    space = False
    while not space:
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN:
                if e.key in (K_ESCAPE, K_q):
                    sys.exit()
                if e.key == K_SPACE:
                    space = True
    entities = pygame.sprite.Group()

    for i in range(18):
        show(Gl.sheet_load.image_at((  0,  360 * i,640,360), Gl.alpha))
        entities.empty()
        Gl.set_camera_and_tiles(make_level(i))
        Gl.levelfinished = False
        player = Player(Gl.spawn_pos[0] * Gl.tile_size, Gl.spawn_pos[1] * Gl.tile_size, entities)
        entities.add(player)
        entities.add(Ball(Gl.ball_golf, Gl.ball_golf_size, Gl.spawn_pos[0] * Gl.tile_size + 20, Gl.spawn_pos[1] * Gl.tile_size, player, entities))
        Gl.level_finished = False

        while not Gl.level_finished:
            Gl.get_input()

            if Gl.input_down and player.bombs > 0:
                player.bombs -= 1
                Gl.input_down = False
                entities.add(Bomb(player.hitbox.center[0], player.hitbox.center[1], player, entities))

            update_entities(player, entities)
            Gl.camera.update(player)
            render(entities)
            Gl.update_fx();
            pygame.display.update()

            Gl.timer.tick(Gl.framerate)
            Gl.framecount += 1


    show(Gl.img_ending)
    finished = False
    while not finished:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN:
                finished = True

if(__name__ == "__main__"):
    main()
