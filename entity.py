import pygame
import pyganim
import spritesheet
from math import sqrt
from config import *



class Entity(pygame.sprite.Sprite):
    def __init__(self, image, x, y, entities):
        pygame.sprite.Sprite.__init__(self)
        self.entities = entities
        self.image = image
        self.rect = image.get_rect().move(x, y)
        self.hitbox = self.rect
        self.hitbox.midbottom = self.rect.midbottom
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.maxvel_x = 0
        self.maxvel_y = 0
        self.fx = Effect(self)
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
            self.vel_x = self.maxvel_x if self.vel_x > 0 else -self.maxvel_x
        if abs(self.vel_y) > self.maxvel_y:
            self.vel_y = self.maxvel_y if self.vel_y > 0 else -self.maxvel_y

        collide_tiles = []
        self.hitbox.x += self.vel_x * Gl.frameincr
        collide_tiles += self.check_collisions_x(self.vel_x)
        self.hitbox.y += self.vel_y * Gl.frameincr
        collide_tiles += self.check_collisions_y(self.vel_y)
        return collide_tiles

    def check_collisions_x(self, vel_x):
        tiles = []
        rows = range(int(self.hitbox.x / Gl.tile_size), int((self.hitbox.x + self.hitbox.w) / Gl.tile_size) + 1)
        cols = range(int(self.hitbox.y / Gl.tile_size), int((self.hitbox.y + self.hitbox.h) / Gl.tile_size) + 1)
        lvl_w = Gl.level_width / Gl.tile_size
        lvl_h = Gl.level_height / Gl.tile_size
        for row in rows:
            if row < 0 or row > lvl_w:
                break
            for col in cols:
                if col < 0 or col > lvl_h:
                    break
                tile = Gl.tiles[col][row]
                if tile and self.hitbox.colliderect(tile.rect):
                    if vel_x > 0:
                        self.vel_x = 0 if not hasattr(self, "bounce") else -self.vel_x * self.bounce
                        if hasattr(self, "bounce_sfx"):
                            self.bounce_sfx.set_volume(self.vel_x / self.maxvel_x) # * self.get_volume_distance())
                            self.bounce_sfx.play()
                        self.hitbox.right = tile.rect.left
                        tiles.append(Gl.tiles[col][row])
                    if vel_x < 0:
                        self.vel_x = 0 if not hasattr(self, "bounce") else -self.vel_x * self.bounce
                        if hasattr(self, "bounce_sfx"):
                            self.bounce_sfx.set_volume(self.vel_y / self.maxvel_y) # * self.get_volume_distance())
                            self.bounce_sfx.play()
                        self.hitbox.left = tile.rect.right
                        tiles.append(Gl.tiles[col][row])
        return tiles

    def check_collisions_y(self, vel_y):
        tiles = []
        floor = pygame.Rect(self.hitbox.left, self.hitbox.bottom, self.hitbox.width, 1)
        floor_collide = False
        rows = range(int(self.hitbox.x / Gl.tile_size), int((self.hitbox.x + self.hitbox.w) / Gl.tile_size) + 1)
        cols = range(int(self.hitbox.y / Gl.tile_size), int((self.hitbox.y + self.hitbox.h) / Gl.tile_size) + 1)
        lvl_w = Gl.level_width / Gl.tile_size
        lvl_h = Gl.level_height / Gl.tile_size
        for row in rows:
            if row < 0 or row > lvl_w:
                break
            for col in cols:
                if col < 0 or col > lvl_h:
                    break
                tile = Gl.tiles[col][row]
                if tile and floor.colliderect(tile.rect):
                    floor_collide = True
                    if hasattr(self, "bounce") and 0 <= vel_y and vel_y < 80:
                        self.isrolling = True
                if tile and self.hitbox.colliderect(tile.rect):
                    if vel_y > 0:
                        self.vel_y = 0 if not hasattr(self, "bounce") else -self.vel_y * self.bounce * (not self.isrolling)
                        if hasattr(self, "bounce_sfx"):
                            self.bounce_sfx.set_volume(self.vel_y / self.maxvel_y) # * self.get_volume_distance())
                            self.bounce_sfx.play()
                        self.hitbox.bottom = tile.rect.top
                        tiles.append(Gl.tiles[col][row])
                        self.inair = False if not hasattr(self, "bounce") else self.hasMomentum
                    if vel_y < 0:
                        self.vel_y = 0 if not hasattr(self, "bounce") else -self.vel_y * self.bounce
                        if hasattr(self, "bounce_sfx"):
                            self.bounce_sfx.set_volume(self.vel_y / self.maxvel_y) # * self.get_volume_distance())
                            self.bounce_sfx.play()
                        self.hitbox.top = tile.rect.bottom
                        tiles.append(Gl.tiles[col][row])
        if not floor_collide:
            self.inair = True
        return tiles

    def get_volume_distance(self):
        distance = sqrt((self.rect.x + Gl.camera.state.center[0])**2 + (self.rect.y + Gl.camera.state.center[1])**2)
        distance = -1 / Gl.win_width * distance + 1
        if (distance < 0):
            distance = 0
        return distance



    def idle(self):
        pass

    def fall(self):
        self.vel_y += self.fall_speed
