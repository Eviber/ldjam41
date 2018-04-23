import pygame
from config import Gl

class Camera(object):
    #camera is a rectangle describing the coordinates of the window within the world space
    def __init__(self, width, height):
        self.state = pygame.Rect(0, 0, width, height)
        self.screenshake_frames = 0
        self.screenshake_x = 0
        self.screenshake_y = 0

    def apply(self, target):
        result = target.move(self.state.topleft)
        if (self.screenshake_frames > 0):
            shake = (self.screenshake_x, self.screenshake_y) if (Gl.framecount % 4 < 2) else (-self.screenshake_x, -self.screenshake_y)
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
        if (self.screenshake_frames > 0):
            self.screenshake_frames -= 1
            if (self.screenshake_frames < self.screenshake_x):
                self.screenshake_x -= 1
            if (self.screenshake_frames < self.screenshake_y):
                self.screenshake_y -= 1
        x = target_rect[0]
        y = target_rect[1]
        xlength = level[2]
        ylength = level[3]
        x = -x + (Gl.win_width / 2)
        y = -y + (Gl.win_height / 2)
        if x > -16:
            x = -16
        if x < -(level.width - Gl.win_width) + 16:
            x = -(level.width - Gl.win_width) + 16
        if y > 0:
            y = 0
        if y < -(level.height - Gl.win_height):
            y = -(level.height - Gl.win_height)
        return pygame.Rect(x, y, xlength, ylength)

    def screenshake(self, duration, force_x, force_y):
        self.screenshake_frames = duration
        self.screenshake_x = force_x
        self.screenshake_y = force_y
        