import pygame, config
from config import *
from player import *

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
        