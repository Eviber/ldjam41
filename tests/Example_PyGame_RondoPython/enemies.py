# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 17:35:12 2013

@author: Romain Alvarez
"""

#   ========== Importation des modules et fichiers analogues ===========

import spritesheet
# module permettant de charger une image en rectangle depuis un fichier bitmap
import pyganim
# module permettant de faire une animation d'image affichable par pygame
from platformer import *
from player import *

#   ================ Definition des variables globales =================

enemysheet = spritesheet.spritesheet("Enemy.png")
# fichier bitmap contenant tous les sprites ennemis

alpha = (185,209,217)
# un tuple contenant les valeurs RGB de la couleur bleue claire utilisée dans Richter.png pour la transparence

#   ================== Definition de la classe Enemy ===================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, facingRight):
        pygame.sprite.Sprite.__init__(self)

        self.xcoord = x
        self.ycoord = y
        # les coordonnées x et y de l'ennemi

        self.xvel = 0
        self.yvel = 0
        # velocité x et y de l'ennemi

        self.facingRight = facingRight



class BonePillar(Enemy):
    """
les squelettes en pile qui crachent du feu
    """
    def __init__(self, x, y, facingRight, delay):
        Enemy.__init__(self, x, y, facingRight)

        self.xcoord = x
        self.ycoord = y
        # les coordonnées x et y de l'ennemi

        self.xvel = 0
        self.yvel = 0
        # velocité x et y de l'ennemi

        self.facingRight = False

        self.idling = True
        self.attacking = False
        self.takingDamage = False
        self.dead = False

        self.idlecount = delay
        self.damagecount = 0

        self.image = enemysheet.image_at((6,470,24,16), alpha)

        self.rect = pygame.Rect(x, y, 24, 16)

        self.invulnerable = False
        self.health = 4
        
        self.fireballs = [0]



    def update(self, playerxcoord, playerycoord):

        if playerxcoord < self.xcoord:
            self.facingRight = False
        if playerxcoord > self.xcoord:
            self.facingRight = True


        if self.idlecount <= 60 or self.idling:
            self.idle()
        if self.idlecount > 60 or self.attacking:
            self.attack()
            
            
        if self.invulnerable:
            self.damagecount += 1
        if not self.invulnerable:
            self.damagecount = 0



        if self.takingDamage:
            self.takedamage(0)


        self.rect.centerx += self.xvel
        self.xcoord = self.rect.topleft[0]
        self.rect.centery += self.yvel
        self.ycoord = self.rect.topleft[1]


        if self.facingRight:
            self.image = transform.flip(self.image, True, False)
            
            
    def idle(self):
        self.attackcount = 0
        self.idlecount += 1
        if self.idlecount < 60:
            self.image = enemysheet.image_at((6,470,24,16), alpha)
        if self.idlecount > 60:
            self.image = enemysheet.image_at((32,470,24,16), alpha)


    def attack(self):
        if self.fireballs[len(self.fireballs)-1] == 1:
            self.fireballs[len(self.fireballs)-1] = 0
        if not self.attacking:
            self.fireballs.append(1)
        self.attacking = True
        self.idlecount = 0
        self.image = enemysheet.image_at((32,470,24,16), alpha)
        if self. attackcount > 10:
            self.attacking = False
        self.attackcount += 1


    def fall(self):
        self.yvel += 0.5
        if self.yvel > 25: self.yvel = 25


    def takedamage(self, damage):
        if not self.takingDamage:
            self.health -= damage
        self.invulnerable = True
        self.image = enemysheet.image_at((58,470,24,16), alpha)
        self.takingDamage = True
        if self.damagecount > 8:
            self.takingDamage = False
            self.invulnerable = False
            if self.health == 0:
                self.dead = True
                self.kill()



class Fireball(Enemy):
    def __init__(self, x, y, facingRight):
        Enemy.__init__(self, x, y, facingRight)

        self.xcoord = x
        self.ycoord = y

        self.xvel = 0
        self.yvel = 0

        self.facingRight = facingRight

        self.growing = False
        self.active = False

        self.image = pygame.Surface((8, 8))

        self.rect = pygame.Rect(x, y, 8, 8)


    def update(self,
               bone_xcoord,
               bone_ycoord,
               bone_attacking,
               bone_facingRight,
               bone_idlecount):


        if not self.active:
            self.rect = pygame.Rect(bone_xcoord, bone_ycoord, 8, 8)
            self.image = pygame.Surface((8, 8))




        if bone_idlecount > 30:
            self.growing = True

        if self.growing:
            if self.facingRight:
                self.rect = pygame.Rect(bone_xcoord+14, bone_ycoord+5, 8, 8)
            if not self.facingRight:
                self.rect = pygame.Rect(bone_xcoord+2, bone_ycoord+5, 8, 8)
            if bone_idlecount > 60:
                self.image = enemysheet.image_at((16,488,8,8), alpha)
            if bone_idlecount > 70:
                self.image = enemysheet.image_at((26,488,8,8), alpha)
            if bone_idlecount > 80:
                self.image = enemysheet.image_at((36,488,8,8), alpha)

        if bone_attacking:
            if not self.active:
                if bone_facingRight:
                    self.xvel = 3
                if not bone_facingRight:
                    self.xvel = -3
            self.growing = False
            self.active = True

        if self.active:
            self.image = enemysheet.image_at((6,488,8,8), alpha)

        if self.xvel < 0:
            self.image = transform.flip(self.image, True, False)


        self.rect.x += self.xvel
        self.rect.y += self.yvel

        self.xcoord = self.rect.topleft[0]
        self.ycoord = self.rect.topleft[1]




class MedusaHead(Enemy):
# les tetes de gorgonne flottantes
    def __init__(self, x, y, facingRight):
        Enemy.__init__(self, x, y, facingRight)
        
        self.moving = True
        self.dying = False
        
        self.goingUp = True
        
        self.image = enemysheet.image_at((6,538,16,16), alpha)
        
        self.rect = pygame.Rect(x, y, 16, 16)

    def update(self):
        
        if self.moving:
            self.move()
        
        if self.dying:
            self.die()
        
        self.rect.centerx += self.xvel
        # incrementer la postion du rectangle d'occupation ennemi en direction x
        self.xcoord = self.rect.topleft[0]
        # mettre à jour la valuer de xcoord
        
        self.rect.centery += self.yvel
        # incrementer la postion du rectangle d'occupation ennemi en direction y
        self.ycoord = self.rect.topleft[1]
        # mettre a jour la valeur de ycoord
        
        if self.yvel < 0:
            self.image = enemysheet.image_at((6,538,16,16), alpha)
        if self.yvel > 0:
            self.image = enemysheet.image_at((24,538,16,16), alpha)
        if self.facingRight:
            self.image = transform.flip(self.image, True, False)
        # si l'ennemi regarde vers la gauche, retourner horizontalement le sprite
        
    def move(self):
        self.moving = True
        if self.facingRight:
            self.xvel = 2
        if not self.facingRight:
            self.xvel = -2
        if self.yvel > 3:
            self.goingUp = True
        if self.yvel < -2:
            self.goingUp = False
        if self.goingUp:
            self.yvel += -0.2
        if not self.goingUp:
            self.yvel += 0.2
        
    def die():
        pass