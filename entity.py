import pygame
import pyganim
import spritesheet

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

    def update(self, tiles, level_width, level_height):
        if (self.inair):
            self.fall()
        else:
            self.idle()
        self.update_rect(tiles, level_width, level_height)

    def update_rect(self, tiles, level_width, level_height):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > level_width:
            self.rect.right = level_width
        if self.rect.bottom > level_height:
            self.rect.bottom = level_height

        if abs(self.vel_x) > self.maxvel_x:
            self.vel_x = self.maxvel_x if self.maxvel_x > 0 else -self.maxvel_x
        if abs(self.vel_y) > self.maxvel_y:
            self.vel_y = self.maxvel_y if self.maxvel_y > 0 else -self.maxvel_y

        self.rect.x += self.vel_x * framerate
        self.hitbox.midbottom = self.rect.midbottom
        self.check_collisions(tiles, self.vel_x, 0)
        self.rect.y += self.vel_y * framerate
        self.hitbox.midbottom = self.rect.midbottom
        self.check_collisions(tiles, 0, self.vel_y)

    def check_collisions(self, tiles, vel_x, vel_y):
        floor = pygame.Rect(self.hitbox.left, self.hitbox.bottom, self.hitbox.width, 1)
        floor_collide = False
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if vel_x > 0:
                    self.hitbox.right = tile.rect.left
                if vel_x < 0:
                    self.hitbox.left = tile.rect.right
                if vel_y > 0:
                    self.vel_y = 0
                    self.hitbox.bottom = tile.rect.top
                    self.inair = False
                if vel_y < 0:
                    self.vel_y = 0
                    self.hitbox.top = tile.rect.bottom
            if (tile.rect.colliderect(floor)):
                floor_collide = True
        if not floor_collide:
            self.inair = True
        self.rect.midbottom = self.hitbox.midbottom

    def idle(self):
        pass

    def fall(self):
        self.vel_y += 12
