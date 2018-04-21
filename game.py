import sys
from pygame import *
from yplayer import *
from random import randint


win_width, win_height = 640, 480

speed = [0, 0]

fillcolor = 20, 20, 20

def main():
    init()
    display.set_icon(image.load("beaugosse.png"))
    display.set_caption("Beaugosse")
    screen = display.set_mode((win_width, win_height), FULLSCREEN)
    lastticks = time.get_ticks()
    player = Player(win_width / 2 + 16, win_height - 64)

    left = False
    right = False
    space = False

    while 1:
        for ev in event.get():
            if ev.type == QUIT: sys.exit()
            if ev.type == KEYDOWN:
                if ev.key in (K_ESCAPE, K_q): sys.exit()
                if ev.key == K_LEFT:
                    left = True
                if ev.key == K_RIGHT:
                    right = True
                if ev.key == K_SPACE:
                    space = True
            elif ev.type == KEYUP:
                if ev.key == K_LEFT:
                    left = False
                if ev.key == K_RIGHT:
                    right = False
                if ev.key == K_SPACE:
                    space = False

        screen.fill(fillcolor)
        player.update(screen, left, right, space)
        display.flip()
        while lastticks + 1000 / 60 > time.get_ticks():
            pass
        lastticks = time.get_ticks()

if __name__ == "__main__":
    main()
