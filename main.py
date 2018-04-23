import sys, pygame, spritesheet, config
from config import *
from pygame import *
from player import *

def toggle_fullscr():
    global fullscr
    global screen
    screen = pygame.display.set_mode(size, 0 if fullscr else FULLSCREEN)
    fullscr = not fullscr

def screenshake(duration, force_x, force_y):
    global screenshake_frames
    global screenshake_x
    global screenshake_y
    screenshake_frames = duration
    screenshake_x = force_x
    screenshake_y = force_y

def get_input():
    global input_down
    global input_left
    global input_up
    global input_right
    global input_A
    global input_B
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == KEYDOWN:
            if e.key in (K_ESCAPE, K_q):
                sys.exit()
            if e.key == K_f or e.key == K_F11:
                toggle_fullscr()
            if e.key == K_UP:
                input_up = True
            if e.key == K_DOWN:
                input_down = True
            if e.key == K_LEFT:
                input_left = True
            if e.key == K_RIGHT:
                input_right = True
            if e.key == K_SPACE:
                input_A = True
            if e.key == K_LALT:
                input_B = True
        if e.type == KEYUP:
            if e.key == K_UP:
                input_up = False
            if e.key == K_DOWN:
                input_down = False
            if e.key == K_LEFT:
                input_left = False
            if e.key == K_RIGHT:
                input_right = False
            if e.key == K_SPACE:
                input_A = False
            if e.key == K_LALT:
                input_B = False

def make_level():
    tiles = []
    tile_x = 0
    tile_y = 0
    for row in level:
        tiles.append([])
        for char in row:
            if char.color == 1:
                tile = tileset[0][0]
            elif char.color == 2:
                tile = tileset[0][1]
            elif char.color == 3:
                tile = tileset[0][2]
            elif char.color == 4:
                tile = tileset[1][0]
            elif char.color == 5:
                tile = tileset[1][1]
            elif char.color == 6:
                tile = tileset[1][2]
            elif char.color == 7:
                tile = tileset[2][0]
            elif char.color == 8:
                tile = tileset[2][1]
            elif char.color == 9:
                tile = tileset[2][2]
            else:
                tile = None
            if tile is not None:
                tiles[tile_y].append(Platform(tile_x * tile_size, tile_y * tile_size, tile))
            tile_x += 1
        tile_x = 0
        tile_y += 1
    return tiles

def render(camera, tiles, entities):
    screen.fill(bgcolor)
    screen.blit(bg, camera.apply_parallax(0, 0, 0.2, 0.2))
    rect = None
    for row in tiles:
        for tile in row:
            rect = camera.apply(tile.rect)
            if (rect.colliderect(screen_rect)):
                screen.blit(tile.image, rect)
    for e in entities:
        rect = camera.apply(e.rect)
        if (rect.colliderect(screen_rect)):
            screen.blit(e.image, rect)


def main():
    init()
    print(level)
    global framecount
    camera = Camera(level_width * tile_size, level_height * tile_size)

    tiles = make_level()
    player = Player(300, 300)
    entities = pygame.sprite.Group()
    entities.add(player)

    ball = Ball(img_ball, 16, 320, 250, player)
    entities.add(ball)

    while True:
        get_input()

        player_status = player.status
        player_landing = player.inair
        player_speed = player.vel_y
        player.update(tiles,
            input_down,
            input_left,
            input_up,
            input_right,
            input_A,
            input_B)
        camera.update(player)
        if player.inair and player.vel_y == 0:
            screenshake(-player_speed / 50, 0, 3)
        if player_landing and not player.inair:
            screenshake(player_speed / 30, 0, 3)
        if player_status == PlayerStatus.golfcharge and player.status == PlayerStatus.golf:
            for e in entities:
                if isinstance(e, Ball) and e.rect.colliderect(player.rect):
                    e.hit(player.golfcharge, player.golfcharge)

        for e in entities:
            if isinstance(e, Ball):
                ball.update(tiles)
            elif not isinstance(e, Player):
                e.update();
        render(camera, tiles, entities)
        pygame.display.update()

        timer.tick(framerate)
        framecount += 1



class Platform(object):
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(x, y, tile_size, tile_size)

class Camera(object):
    #camera is a rectangle describing the coordinates of the window within the world space
    def __init__(self, width, height):
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        result = target.move(self.state.topleft)
        if (screenshake_frames > 0):
            shake = (screenshake_x, screenshake_y) if (framecount % 4 < 2) else (-screenshake_x, -screenshake_y)
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
        global screenshake_frames
        global screenshake_x
        global screenshake_y
        if (screenshake_frames > 0):
            screenshake_frames -= 1
            if (screenshake_frames < screenshake_x):
                screenshake_x -= 1
            if (screenshake_frames < screenshake_y):
                screenshake_y -= 1
        xcoord = target_rect[0]
        ycoord = target_rect[1]
        xlength = level[2]
        ylength = level[3]
        xcoord = -xcoord + (win_width/2)
        ycoord = -ycoord + (win_height/2)
        if xcoord > -16:
            xcoord = -16
        if xcoord < -(level.width-win_width)+16:
            xcoord = -(level.width-win_width)+16
        if ycoord > 0:
            ycoord = 0
        if ycoord < -(level.height-win_height):
            ycoord = -(level.height-win_height)
        return pygame.Rect(xcoord, ycoord, xlength, ylength)



if(__name__ == "__main__"):
    main()
