import pygame
import pyganim
import spritesheet
from config import *

framerate = 1 / (1000/60)

class Entity(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect().move(x, y)
        self.hitbox = self.rect
        self.hitbox.midbottom = self.rect.midbottom
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.maxvel_x = 0
        self.maxvel_y = 0
        self.fall_speed = 12
        self.flip = False
        self.inair = True

    def update(self):
        if (self.inair):
            self.fall()
        else:
            self.idle()
        self.update_rect()

    def update_rect(self):
        lvl_w = Gl.level_width * Gl.tile_size
        lvl_h = Gl.level_height * Gl.tile_size
        if (self.hitbox.left < 0):
            self.hitbox.left = 0
        if (self.hitbox.right > lvl_w):
            self.hitbox.right = lvl_w
        if (self.hitbox.bottom > lvl_h):
            self.hitbox.bottom = lvl_h

        if abs(self.vel_x) > self.maxvel_x:
            self.vel_x = self.maxvel_x if self.maxvel_x > 0 else -self.maxvel_x
        if abs(self.vel_y) > self.maxvel_y:
            self.vel_y = self.maxvel_y if self.maxvel_y > 0 else -self.maxvel_y

        self.hitbox.x += self.vel_x * framerate
        self.check_collisions_x(self.vel_x)
        self.hitbox.y += self.vel_y * framerate
        self.check_collisions_y(self.vel_y)

    def check_collisions_x(self, vel_x):
        for row in range(-int(Gl.camera.state.x / Gl.tile_size), -int((Gl.camera.state.x - Gl.win_width) / Gl.tile_size) + 1):
            for col in range(-int(Gl.camera.state.y / Gl.tile_size), -int((Gl.camera.state.y - Gl.win_height) / Gl.tile_size) + 1):
                tile = Gl.tiles[col][row]
                if tile and self.hitbox.colliderect(tile.rect):
                    if vel_x > 0:
                        self.vel_x = 0 if not hasattr(self, "bounce_x") else -self.vel_x * self.bounce_x
                        self.hitbox.right = tile.rect.left
                        if hasattr(self, "bounce"):
                            self.vel_x = -self.vel_x * 0.5
                    if vel_x < 0:
                        self.vel_x = 0 if not hasattr(self, "bounce_y") else -self.vel_x * self.bounce_x
                        self.hitbox.left = tile.rect.right
                        if hasattr(self, "bounce"):
                            self.vel_x = -self.vel_x * 0.5
        self.rect.midbottom = self.hitbox.midbottom

    def check_collisions_y(self, vel_y):
        floor = pygame.Rect(self.hitbox.left, self.hitbox.bottom, self.hitbox.width, 1)
        floor_collide = False
        for row in range(-int(Gl.camera.state.x / Gl.tile_size), -int((Gl.camera.state.x - Gl.win_width) / Gl.tile_size) + 1):
            for col in range(-int(Gl.camera.state.y / Gl.tile_size), -int((Gl.camera.state.y - Gl.win_height) / Gl.tile_size) + 1):
                tile = Gl.tiles[col][row]
                if tile and self.hitbox.colliderect(tile.rect):
                    if vel_y > 0:
                        self.vel_y = 0
                        if hasattr(self, "bounce"):
                            self.vel_y = -self.vel_y * 0.7 + 12 if self.hasMomentum else 0
                        self.vel_y = 0 if not hasattr(self, "bounce_x") else -self.vel_y * self.bounce_y
                        self.hitbox.bottom = tile.rect.top
                        self.inair = False
                    if vel_y < 0:
                        self.vel_y = 0 if not hasattr(self, "bounce_y") else -self.vel_y * self.bounce_y
                        self.hitbox.top = tile.rect.bottom
                if tile and floor.colliderect(tile.rect):
                    floor_collide = True
        if not floor_collide:
            self.inair = True

    def idle(self):
        pass

    def fall(self):
        self.vel_y += self.fall_speed
