import pygame
import pyganim
import spritesheet
from config import *


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
        self.bounce_threshold = 10

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
        for row in range(int(self.hitbox.x / Gl.tile_size), int((self.hitbox.x + self.hitbox.w) / Gl.tile_size) + 1):
            for col in range(int(self.hitbox.y / Gl.tile_size), int((self.hitbox.y + self.hitbox.h) / Gl.tile_size) + 1):
                tile = Gl.tiles[col][row]
                if tile and self.hitbox.colliderect(tile.rect):
                    if vel_x > 0:
                        self.vel_x = 0 if not hasattr(self, "bounce_x") else -self.vel_x * self.bounce_x
                        if hasattr(self, "bounce_sfx"):
                            #distance = math.sqrt((self.rect.x - Gl.camera.state.center.x)**2 + (self.rect.y - Gl.camera.state.center.y)**2)
                            self.bounce_sfx.set_volume(self.vel_x / self.maxvel_x)
                            self.bounce_sfx.play()
                        self.hitbox.right = tile.rect.left
                        tiles.append(Gl.tiles[col][row])
                    if vel_x < 0:
                        self.vel_x = 0 if not hasattr(self, "bounce_x") else -self.vel_x * self.bounce_x
                        if hasattr(self, "bounce_sfx"):
                            self.bounce_sfx.set_volume(self.vel_y / self.maxvel_y)
                            self.bounce_sfx.play()
                        self.hitbox.left = tile.rect.right
                        tiles.append(Gl.tiles[col][row])
        return tiles

    def check_collisions_y(self, vel_y):
        tiles = []
        floor = pygame.Rect(self.hitbox.left, self.hitbox.bottom, self.hitbox.width, 1)
        floor_collide = False
        for row in range(int(self.hitbox.x / Gl.tile_size), int((self.hitbox.x + self.hitbox.w) / Gl.tile_size) + 1):
            for col in range(int(self.hitbox.y / Gl.tile_size), int((self.hitbox.y + self.hitbox.h) / Gl.tile_size) + 1):
                tile = Gl.tiles[col][row]
                if tile and self.hitbox.colliderect(tile.rect):
                    if vel_y > 0:
                        self.vel_y = 0 if not hasattr(self, "bounce_y") else -self.vel_y * self.bounce_y
                        if hasattr(self, "bounce_sfx"):
                            self.bounce_sfx.set_volume(self.vel_y / self.maxvel_y)
                            self.bounce_sfx.play()
                        self.hitbox.bottom = tile.rect.top
                        tiles.append(Gl.tiles[col][row])
                        self.inair = False
                    if vel_y < 0:
                        self.vel_y = 0 if not hasattr(self, "bounce_y") else -self.vel_y * self.bounce_y
                        if hasattr(self, "bounce_sfx"):
                            self.bounce_sfx.set_volume(self.vel_y / self.maxvel_y)
                            self.bounce_sfx.play()
                        self.hitbox.top = tile.rect.bottom
                        tiles.append(Gl.tiles[col][row])
                if tile and floor.colliderect(tile.rect):
                    floor_collide = True
        if not floor_collide:
            self.inair = True
        return tiles

    def idle(self):
        pass

    def fall(self):
        self.vel_y += self.fall_speed
