import pygame
import pyganim
import spritesheet
from config import *

framerate = 1 / (1000/60)

class Entity(pygame.sprite.Sprite):
    def __init__(self, image, size, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = pygame.Rect(x, y, size, size)
        self.hitbox = self.rect
        self.hitbox.midbottom = self.rect.midbottom
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.maxvel_x = 0
        self.maxvel_y = 0

        self.flip = False
        self.inair = True

    def update(self):
        if (self.inair):
            self.fall()
        else:
            self.idle()
        self.update_rect(Gl.tiles)

    def update_rect(self):
        lvl_w = Gl.level_width * Gl.tile_size
        lvl_h = Gl.level_height * Gl.tile_size
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > lvl_w:
            self.rect.right = lvl_w
        if self.rect.bottom > lvl_h:
            self.rect.bottom = lvl_h

        if abs(self.vel_x) > self.maxvel_x:
            self.vel_x = self.maxvel_x if self.maxvel_x > 0 else -self.maxvel_x
        if abs(self.vel_y) > self.maxvel_y:
            self.vel_y = self.maxvel_y if self.maxvel_y > 0 else -self.maxvel_y

        self.rect.x += self.vel_x * framerate
        self.check_collisions_x(self.vel_x)
        self.rect.y += self.vel_y * framerate
        self.check_collisions_y(self.vel_y)

    def check_collisions_x(self, vel_x):
        self.hitbox.midbottom = self.rect.midbottom
        for row in Gl.tiles:
            for tile in row:
                if self.hitbox.colliderect(tile.rect):
                    if vel_x > 0:
                        self.hitbox.right = tile.rect.left
                        if hasattr(self, "bounce"):
                            self.vel_x = -self.vel_x * 0.6
                    if vel_x < 0:
                        self.hitbox.left = tile.rect.right
                        if hasattr(self, "bounce"):
                            self.vel_x = -self.vel_x * 0.6
        self.rect.midbottom = self.hitbox.midbottom

    def check_collisions_y(self, vel_y):
        self.hitbox.midbottom = self.rect.midbottom
        floor = pygame.Rect(self.hitbox.left, self.hitbox.bottom, self.hitbox.width, 1)
        floor_collide = False
        for row in Gl.tiles:
            for tile in row:
                if self.hitbox.colliderect(tile.rect):
                    if vel_y > 0:
                        self.vel_y = 0 if not hasattr(self, "bounce") else -self.vel_y * 0.7
                        self.hitbox.bottom = tile.rect.top
                        self.inair = False
                    if vel_y < 0:
                        self.vel_y = 0 if not hasattr(self, "bounce") else -self.vel_y * 0.7
                        self.hitbox.top = tile.rect.bottom
                if (floor.colliderect(tile.rect)):
                    floor_collide = True
        if not floor_collide:
            self.inair = True
        self.rect.midbottom = self.hitbox.midbottom

    def idle(self):
        pass

    def fall(self):
        self.vel_y += 12
