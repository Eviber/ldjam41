# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:25:47 2013

@author: Alexis Duquesne
"""

# Ce fichier contient la classe Player qui est le joueur
# ainsi que la sous-classe Attack qui gere les hitbox des attaques
# et la sous-classe ItemAxe qui gere les haches de lancer

#   ========== Importation des modules et fichiers analogues ===========

import spritesheet
# module permettant de charger une image en rectangle depuis un fichier bitmap
import pyganim
# module permettant de faire une animation d'image affichable par pygame
from platformer import *
from enemies import *

#   ================ Definition des variables globales =================

richtersheet = spritesheet.spritesheet("Richter.png")
# la spritesheet du joueur : toutes les frames d'animation de celui-ci

axesheet = spritesheet.spritesheet("Bridge.png")
# charger le fichier contenant les images necessaires au sprite hache

alpha = (185,209,217)
# un tuple contenant les valeurs RGB de la couleur bleue claire utilisée dans Richter.png pour la transparence

#   =================== Definition du sprite joueur ====================

class Player(pygame.sprite.Sprite):
# classe du joueur, qui est un sprite donc qui en herite les attributs
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
#   ============== Affectation des attributs de la classe ==============

        self.attack = self.Attack(x, y)
        # creer l'instance de la classe Attack qui gere les attaques du joueur
        self.axe1 = self.ItemAxe(x, y)
        self.axe2 = self.ItemAxe(x, y)
        # creer deux instances de haches qui peuvent etre lancées par le joueur


        self.xcoord = x
        self.ycoord = y
        # coordonnees du sprite joueur

        self.xvel = 0
        self.yvel = 0
        # velocité x et y du joueur (en pixels par frame)


        self.facingRight = True
        # si le joueur regarde a droite ou pas (afin de retourner les images)
        self.onGround = True
        # si le joueur touche le sol
        self.invulnerable = False
        # si le joueur ne peut pas prendre des degats

        self.takingDamage = False
        # si le joueur est en train d'etre ejecte par un ennemi
        self.idling = True
        # si le joueur ne fait rien
        self.walking = False
        # si le joueur est en train de marcher au sol
        self.taunting = False
        # si le joueur est en train de se la peter (appuyer sur haut)
        self.crouching = False
        # si le joueur est accroupi
        self.jumping = False
        # si le joueur est en train de sauter
        self.backdashing = False
        # si le joueur est en train de faire une esquive arriere
        self.backflipping = False
        # si le joueur est en train de faire un salto arriere
        self.whipping = False
        # si le joueur est en train d'attaquer au fouet
        self.usingitem = False
        # si le joueur est en train de lancer un item
        self.jumpwhipping = False
        # si le joueur est en train d'attaquer au fouet en l'air
        self.jumpusingitem = False
        # si le joueur est en train de lancer un item en l'air
        self.sliding = False
        # si le joueur est en train de glisser sur le sol
        self.slidekicking = False
        # si le joueur effectue l'attaque du coup de pied glissade aerien


        self.axelist = [0, 0]
        # cette liste repere les nombre de haches à l'ecran afin de les limiter a deux et de les instancier correctement

        self.jumped = False
        self.backdashed = False
        self.backflipped = False
        self.whipped = False
        self.slided = False
        self.slidekicked = False
        self.useditem = False
        # ces variables servent a empecher que le joueur puisse repeter l'action a l'infini en gardant la touche enfoncée


        self.image = richtersheet.image_at((2,2,16,32), alpha)
        # ceci est l'image representant le joueur a tout moment, d'abord affecté a la pose debout fixe
        self.elapsed = None
        # à ou en est l'animation actuelle du joueur (en secondes ; est None si l'image n'est pas animée)

        self.rect = pygame.Rect(x, y, 16, 32)
        # la rectangle d'occupation du joueur, qui va detecter les collisions avec les murs, etc
        self.hitbox = pygame.Rect(x+2, y+2, 12, 30)
        # la hitbox du joueur qui va detecter les collisions avec les ennemis, plus petit que rect


        self.health = 20
        # points de vie du joueur, si cette valeur atteint zero alors le joueur est mort
        self.healthList = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        # une liste pour representer la barre de vie du joueur afin d'etre affichee

        self.score = 0
        # le score du joueur
        self.scoreString = "000000"
        # chaine de 6 caracteres pour l'affichage a l'ecran du score du joueur

        self.ammo = 20
        # quantités de munitions pour les haches du joueur

        self.item = "AXE"
        # type d'objet a munitions que le joueur detient
        
#   =============== Definition des animations du joueur ================
        
# a l'aide du module PygAnim
		
        self.animWalk = pyganim.PygAnimation([
            (richtersheet.image_at((2,138,16,32), alpha), 0.2),
            (richtersheet.image_at((20,138,16,32), alpha), 0.2),
            (richtersheet.image_at((38,138,16,32), alpha), 0.2),
            (richtersheet.image_at((56,138,16,32), alpha), 0.2)])
        # animation de marche du joueur
		
        self.animBackdash = pyganim.PygAnimation([
            (richtersheet.image_at((2,648,16,32), alpha), 0.05),
            (richtersheet.image_at((20,648,16,32), alpha), 0.05),
            (richtersheet.image_at((38,648,24,32), alpha), 0.3),
            (richtersheet.image_at((64,648,16,32), alpha), 0.1)], False)
        self.animBackdash.loop = False
        # animation d'esquive arriere
		
        self.animBackflip = pyganim.PygAnimation([
            (richtersheet.image_at((2,580,16,32), alpha), 0.06),
            (richtersheet.image_at((20,580,24,32), alpha), 0.1),
            (richtersheet.image_at((46,580,24,32), alpha), 0.1),
            (richtersheet.image_at((72,580,24,32), alpha), 0.06),
            (richtersheet.image_at((98,580,32,32), alpha), 0.08),
            (richtersheet.image_at((132,580,24,32), alpha), 0.1)], False)
        self.animBackflip.loop = False
        # animation de salto arriere
        
        self.animWhipGround = pyganim.PygAnimation([
            (richtersheet.image_at((18,206,16,32), alpha), 0.1),
            (richtersheet.image_at((60,206,16,32), alpha), 0.05),
            (richtersheet.image_at((78,206,16,32), alpha), 0.05),
            (richtersheet.image_at((136,206,16,32), alpha), 0.2),
            (richtersheet.image_at((202,206,16,32), alpha), 0.05)], False)
        self.animWhipGround.loop = False
        # animation d'attaque fouet au sol du joueur
        self.animWhipCrouch = pyganim.PygAnimation([
            (richtersheet.image_at((18,308,16,32), alpha), 0.1),
            (richtersheet.image_at((60,308,16,32), alpha), 0.05),
            (richtersheet.image_at((78,308,16,32), alpha), 0.05),
            (richtersheet.image_at((136,308,16,32), alpha), 0.2),
            (richtersheet.image_at((202,308,16,32), alpha), 0.05)], False)
        self.animWhipCrouch.loop = False
        # animation d'attaque fouet du joueur accroupi
        self.animWhipJump = pyganim.PygAnimation([
            (richtersheet.image_at((18,410,16,32), alpha), 0.1),
            (richtersheet.image_at((60,410,16,32), alpha), 0.05),
            (richtersheet.image_at((78,410,16,32), alpha), 0.05),
            (richtersheet.image_at((136,410,16,32), alpha), 0.2),
            (richtersheet.image_at((202,410,16,32), alpha), 0.05)], False)
        self.animWhipJump.loop = False
        # animation d'attaque fouet du joueur en l'air
        
        self.animItemGround = pyganim.PygAnimation([
            (richtersheet.image_at((10,274,16,32), alpha), 0.1),
            (richtersheet.image_at((28,274,16,32), alpha), 0.05),
            (richtersheet.image_at((46,274,16,32), alpha), 0.05),
            (richtersheet.image_at((72,274,16,32), alpha), 0.15)], False)
        self.animItemGround.loop = False
        # animation de lancer de hache au sol du joueur
        self.animItemJump = pyganim.PygAnimation([
            (richtersheet.image_at((10,444,16,32), alpha), 0.1),
            (richtersheet.image_at((28,444,16,32), alpha), 0.05),
            (richtersheet.image_at((46,444,16,32), alpha), 0.05),
            (richtersheet.image_at((72,444,16,32), alpha), 0.15)], False)
        self.animItemJump.loop = False
        # animation de lancer de hache du joueur en l'air
        
        self.animSlide = pyganim.PygAnimation([
            (richtersheet.image_at((2,512,16,32), alpha), 0.05),
            (richtersheet.image_at((28,512,16,32), alpha), 0.05),
            (richtersheet.image_at((62,512,16,32), alpha), 0.3),
            (richtersheet.image_at((96,512,16,32), alpha), 0.1),
            (richtersheet.image_at((130,512,16,32), alpha), 0.1)], False)
        self.animSlide.loop = False
        # animation de glissage au sol du joueur
        
        self.animSlidekick = pyganim.PygAnimation([
            (richtersheet.image_at((2,546,16,32), alpha), 0.1),
            (richtersheet.image_at((36,546,16,32), alpha), 0.4),
            (richtersheet.image_at((70,546,16,32), alpha), 0.1),
            (richtersheet.image_at((104,546,16,32), alpha), 0.1),
            (richtersheet.image_at((138,546,16,32), alpha), 0.1),
            (richtersheet.image_at((164,546,16,32), alpha), 0.1),
            (richtersheet.image_at((182,546,16,32), alpha), 0.1)], False)
        self.animSlidekick.loop = False
        # animation de coup de pied aerien du joueur
		
#   ======================= Fonction Mise a jour =======================
	
    def update(self,
               up, releaseUp,
               down, releaseDown,
               left, releaseLeft,
               right, releaseRight,
               Abutton, releaseAbutton,
               Bbutton, releaseBbutton,
               Lbutton, releaseLbutton,
               Rbutton, releaseRbutton,
               platforms, enemies):
    # fonction de mise a jour du joueur, joue le lien avec toutes les autres fonctions
               
        self.elapsed = None
        # est reglé d'abord sur None à chaque frame pour la stabilité de la valeur
        
#   ======================= Conditions d'action ========================

        if not self.onGround:
            self.fall()
        # mettre en oeuvre la gravité si le joueur n'est pas au sol
            
        if up or down or left or right or Abutton or Bbutton or Lbutton or Rbutton:
            self.idling = False
            # si un bouton est enfoncé, le joueur n'est plus fixe
        
        if not down:
            self.crouching = False
            # si bas n'est pas enfoncé, n'est forcement pas accroupi
            
        if not (self.backdashing or
                self.backflipping or
                self.whipping or
                self.usingitem or
                self.sliding or
                self.slidekicking or
                self.takingDamage):
        # si le joueur n'est pas en train d'effectuer des actions prioritaires

            if (left or right):
                self.walk(left, right)
            # si l'on appuye sur gauche ou droite, le faire marcher dans la dite direction
            if (releaseLeft or releaseRight):
                self.walking = False
            # arreter de marcher si les touches sont relachées

            if Abutton and not self.crouching:
                self.jump()
            # si l'on appuye sur A lorsque le joueur n'est pas accroupi, le faire sauter

            if up and Bbutton and not self.useditem and self.ammo > 0 and self.axelist != [1,1]:
                self.useitem()
            # si l'on appuye sur haut et B en ayant des munitions et moins de 2 haches a l'ecran, envoyer une hache

            if Bbutton and not self.whipped and not self.usingitem:
                self.whipattack()
            # si l'on appuye sur B, le faire attaquer au fouet


            if not self.onGround:
                if Lbutton and not self.backflipped:
                    self.backflip()
                # si l'on appuye sur L en l'air, faire un salto arriere


            if self.onGround:
            # si le joueur est au sol
                if not(up or down or left or right or Abutton or Bbutton):
                    self.idle()
                # si aucune touche n'est enfoncée, le mettre en etat fixe

                if up and not self.walking:
                    self.taunt()
                # si l'on appuye sur haut, lui faire prendre la pose

                if down:
                    self.crouch()
                # si l'on appuye sur bas, le faire s'accroupir
                    
                if Lbutton and not self.backdashed:
                    self.backdash()
                # si l'on appuye sur L au sol, faire une esquive arriere

                if Abutton and self.crouching and not self.slided:
                    self.slide()
                # si l'on appuye sur A lorsque le joueur est accroupi, le faire glisser
                    
        if Abutton and self.sliding and self.animSlide.elapsed > 0.2 and not self.slidekicked:
            self.slidekick()
        # si l'on appuye sur A pendant une glissade, le faire faire un slidekick

#   ==================== Reautoriser les actions =======================

        if not Abutton and self.onGround:
            self.jumped = False
        if not Lbutton and not self.backdashing:
            self.backdashed = False
        if not Lbutton and self.onGround:
            self.backflipped = False
        if not Bbutton and not self.whipping:
            self.whipped = False
        if not Bbutton and not self.usingitem and self.axelist != [1, 1]:
            self.useditem = False
        if not Abutton and not self.sliding:
            self.slided = False
        if not Abutton and not self.slidekicking:
            self.slidekicked = False
        # ces variables (en "ed") permettent en fait de verifier que le joueur a bien relaché la touche
        # afin qu'il ne puisse pas garder le bouton appuyé pour repeter l'action a l'infini

#   ============== Lire les fonctions d'action en cours ================

        if self.backdashing:
            self.backdash()
        if self.backflipping:
            self.backflip()
        if self.whipping:
            self.whipattack()
        if self.usingitem:
            self.useitem()
        if self.sliding:
            self.slide()
        if self.slidekicking:
            self.slidekick()
        if self.takingDamage:
            self.takedamage()
        # si l'action est en cours, executer la fonction correspondante a cette frame

#   =============== Deplacement du sprite et collisions ================

        self.rect.x += self.xvel
        # incrementer la postion du rect d'occupation joueur en direction x
        self.xcoord = self.rect.x
        # mettre à jour la valuer de xcoord
        self.collidewall(self.xvel, 0, platforms)

        self.rect.y += self.yvel
        # incrementer la postion du rect d'occupation joueur en direction y
        self.ycoord = self.rect.y
        # mettre a jour la valeur de ycoord
        self.collidewall(0, self.yvel, platforms)
        # verifier les collisions avec les murs

        self.collideenemy(enemies)
        # verifier les collisions avec les ennemis

#   ====================== Mise a jour de la hitbox ====================

        if (self.takingDamage or
            self.idling or
            self.walking or
            self.taunting or
            self.jumping or
            self.backdashing or
            self.backflipping or
            self.whipping or
            self.jumpwhipping or
            self.usingitem or
            self.jumpusingitem):
            self.hitbox = pygame.Rect(self.xcoord+2, self.ycoord+2, 12, 30)
            
        if (self.crouching):
            self.hitbox = pygame.Rect(self.xcoord+2, self.ycoord+16, 12, 16)
            
        if (self.sliding or
            self.slidekicking):
            self.hitbox = pygame.Rect(self.xcoord+2, self.ycoord+18, 12, 14)

#   =================== Reglage de l'image joueur ======================

        if isinstance(self.image, pyganim.PygAnimation):
            self.elapsed = self.image.elapsed
            self.image = self.image.getCurrentFrame()
        # si l'image joueur est un objet animation (que pygame ne peut pas dessiner a l'ecran)
        # alors le transformer en objet surface, et noter ou en est son animation dans elapsed
        if not self.facingRight:
            self.image = transform.flip(self.image, True, False)
        # si le joueur regarde vers la gauche, retourner horizontalement le sprite

#   ================== Imposer des limites aux valeurs =================

        self.health = max(0, self.health)
        self.health = min(16, self.health)
        self.score = max(0, self.score)
        self.score = min(999999, self.score)
        self.ammo = max(0, self.ammo)
        self.ammo = min(99, self.ammo)
        # le joueur doit avoir entre 0 et 16 points de vie
        # et entre 0 et 99 points de munitions

#   ============= Mise a jour des valeurs d'affichage HUD ==============

        for n in range(17):
            if self.health == n:
                for i in range(n):
                    self.healthList[i] = 1
                for j in range(16-n):
                    self.healthList[n+j] = 0
        # on transforme la valeur numerique des points de vie du joueur
        # en liste pour afficher la barre de vie, il y a 16 elements dans celle-ci

        self.scoreString = "0" * (6 - len(str(self.score))) + str(self.score)
        # on convertit la valeur numerique du score en string a 6 caracteres
        # score etant inferieur a 999999

#   ================== Mise a jour des sous-classes ====================

        self.attack.update(self.crouching,
                           self.whipping,
                           self.usingitem,
                           self.sliding,
                           self.slidekicking,
                           self.facingRight,
                           self.elapsed,
                           self.xcoord, self.ycoord,
                           enemies)
        # mettre a jour l'objet attack
        
        if self.axelist[0] == 1:
            self.axe1.update(self.elapsed, self.facingRight,
                             self.usingitem, self.useditem,
                             self.xcoord, self.ycoord,
                             enemies)
        if self.axelist[1] == 1:
            self.axe2.update(self.elapsed, self.facingRight,
                             self.usingitem, self.useditem,
                             self.xcoord, self.ycoord,
                             enemies)
        # mettre a jour les objets haches si elles sont censées etre a l'ecran

#   ===================== Fonctions d'actions joueur ===================

    def collidewall(self, xvel, yvel, platforms):
        """
    verifie les collisions du joueur aux murs et l'empeche de les traverser
        """
        collideUnder = 0
        # cette variable verifie s'il y a bien une plateforme solide sous les pieds du joueur
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
            # boucle: pour tout p dans la liste des plateformes solides du terrain
            # si il y a collision entre le rect joueur et le rect plateforme
                if xvel > 0:
                    self.rect.right = p.rect.left
                    # si le joueur va vers la droite
                    # replacer le rect joueur au bord gauche du rect plateforme
                if xvel < 0:
                    self.rect.left = p.rect.right
                    # si le joueur va vers la gauche
                    # replacer le rect joueur au bord droit du rect plateforme
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.jumping = False
                    self.yvel = 0
                    # si le joueur va vers le bas
                    # replacer le rect joueur au bord haut du rect plateforme
                    # le joueur est donc au sol et n'est plus en train de sauter
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    # si le joueur va vers le haut
                    # replacer le rect joueur au bord bas du rect plateforme
                    # il descend desormais
            if p.rect.collidepoint(self.rect.left, self.rect.bottom) or p.rect.collidepoint(self.rect.right, self.rect.bottom):
                collideUnder += 1
                # si en dessous du bord droit ou du bord gauche du rect joueur il y a une plateforme
                # ajouter 1 a la variable des collisions sous le joueur
            if self.slidekicking and self.animSlidekick.elapsed <= 0.7:
                if  ((self.facingRight and p.rect.collidepoint(self.rect.right+14, self.rect.centery)) or
                    (not self.facingRight and p.rect.collidepoint(self.rect.left-14, self.rect.centery))):
                    self.slidekicking = False
                    self.animSlidekick.stop()
                    self.backflip()
                # si le joueur fait un slidekick et touche un mur, lui faire faire un salto arriere
        if collideUnder==0:
            self.onGround = False
            # si a l'issue de la boucle il n'y a pas eu de plateforme detectee sous le joueur
            # le joueur n'est donc pas au sol

    def collideenemy(self, enemies):
        """
    verifie les collisions du joueur aux ennemis et lui fait prendre des degats
        """
        for n in enemies:
            if self.hitbox.colliderect(n.rect):
            # boucle: pour tout n dans la liste des ennemis a l'ecran
            # si il y a collision entre le rect joueur et le rect ennemi
                self.takedamage(1)


    def idle(self):
        """
    fait que le joueur reste debout, fixe
    est lancée si aucun bouton n'est enfoncé
        """
        self.image = richtersheet.image_at((2,2,16,32), alpha)
        # l'image est mise sur la pose fixe du personnage
        if self.taunting:
            self.image = richtersheet.image_at((2,36,16,32), alpha)
            # faire la frame de transition si l'on appuyait sur haut avant
        if self.crouching:
            self.image = richtersheet.image_at((2,70,16,32), alpha)
            # faire la frame de transition s'il etait accroupi
        self.idling = True
        self.taunting = False
        self.crouching = False
        self.xvel = 0


    def taunt(self):
        """
    met le joueur en etat d'attaques altérées (haches)
    est lancée si haut est enfoncé
        """
        if not self.taunting:
            self.image = richtersheet.image_at((2,36,16,32), alpha)
            # faire la frame de transition
        if self.taunting:
            self.image = richtersheet.image_at((20,36,16,32), alpha)
            # l'image joueur est mise sur la pose du taunt (de dos)
        self.taunting = True
        self.idling = False
        self.crouching = False
        self.xvel = 0
        # il ne peut pas bouger si haut est enfoncé


    def crouch(self):
        """        
    fait s'accroupir le joueur
    est lancée si bas est enfoncé
        """
        if not self.crouching:
            self.image = richtersheet.image_at((2,70,16,32), alpha)
            # faire la frame de transition
        if self.crouching:
            self.image = richtersheet.image_at((20,70,16,32), alpha)
            # l'image joueur est mise sur la pose accroupie
        self.crouching = True
        self.idling = False
        self.taunting = False
        self.xvel = 0
        # il ne peut pas bouger en etant accroupi


    def walk(self, left, right):
        """
    fait avancer (marcher s'il est au sol) le joueur a droite ou a gauche
    est lancée si droite ou gauche sont enfoncés
        """
        self.walking = True
        if right:
            self.xvel = 2
            # si on marche a droite, le joueur va a droite a 2 pixels par frame
            if not self.facingRight:
                self.facingRight = True
                # si le joueur ne regardait pas vers la droite avant, maintenant oui
            if self.onGround:
                self.image = self.animWalk
                self.animWalk.play()
                # si le joueur est au sol, l'image joueur est mise sur l'animation de marche du joueur
        if left:
            self.xvel = -2
            if self.facingRight:
                self.facingRight = False
            if self.onGround:
                self.image = self.animWalk
                self.animWalk.play()
        if not self.walking:
            self.animWalk.stop()
            # arreter l'animation si le joueur ne marche pas


    def jump(self):
        """
    fait sauter en l'air le joueur
    est lancée si A est enfoncé
        """
        if self.onGround and not self.jumped:
            self.yvel = -5
            # le joueur va vers le haut a 5 pixels par frame
            self.jumping = True
            self.jumped = True
            self.onGround = False
            self.crouching = False
            self.taunting = False
        if self.jumped and self.yvel < 0:
            self.yvel -= 0.2
            # s'il va vers le haut, la velocité verticale est augmentée de 0.2 vers le haut
            # (ceci sert a faire sauter un peu plus haut le joueur si A est enfoncé plus longtemps)


    def fall(self):
        """
    fonction pour appliquer la gravité au joueur
    est lancée si le joueur n'est pas au sol
        """
        self.yvel += 0.5
        # acceleration vers le bas due à la gravité
        if self.yvel > 25: self.yvel = 25
        # vitesse de chute maximale
        if self.yvel < 0:
            if self.xvel == 0:
                self.image = richtersheet.image_at((2,104,16,32), alpha)
            else:
                self.image = richtersheet.image_at((20,104,16,32), alpha)
            # si le joueur va vers le haut
            # l'image joueur est mise sur la pose saut vertical s'il ne vas pas a droite ou gauche
            # sinon, l'image joueur est mise sur la pose du saut en avant
        if 2 >= self.yvel >= 0:
            self.image = richtersheet.image_at((38,104,16,32), alpha)
            # si le joueur est au sommet de son saut
            # l'image joueur est mise sur la pose en suspens en l'air
        if self.yvel > 2:
            self.image = richtersheet.image_at((56,104,16,32), alpha)
            # si le joueur descend
            # l'image joueur est mise sur la pose descendante


    def backdash(self):
        """
    fait faire au joueur une esquive en arriere
    est lancée si l'on appuye sur L au sol
        """
        self.backdashing = True
        self.backdashed = True
        self.image = self.animBackdash
        if self.animBackdash.elapsed < 0.2:
            self.xvel = 3
        elif self.animBackdash.elapsed < 0.4:
            self.xvel = 1
        else:
            self.xvel = 0
        if self.facingRight and self.xvel > 0:
            self.xvel *= -1
        # regler la vitesse en fonction d'ou il en est de l'animation
        if self.animBackdash.isFinished():
            self.backdashing = False
            self.animBackdash.stop()
            self.image = richtersheet.image_at((82,648,16,32), alpha)
        if self.backdashing:
            self.animBackdash.play()


    def backflip(self):
        """
    fait faire au joueur un salto arriere
    est lancée si l'on appuye sur L en l'air, ou si l'on touche un mur en faisant un slidekick
        """
        if not self.backflipping:
            self.yvel = -3
            # si c'est la premiere fois que cette fonction est lue, le joueur saute legerement
        self.backflipping = True
        self.backflipped = True
        self.image = self.animBackflip
        self.onGround = False
        if self.facingRight:
            self.xvel = -2
        if not self.facingRight:
            self.xvel = 2
            # le faire aller en arriere a 2 pix/frame
        if self.animBackflip.isFinished():
            self.backflipping = False
            self.animBackflip.stop()
            self.image = richtersheet.image_at((38,104,16,32), alpha)
            # si il a fait un salto (animation terminée), arreter de lire la fonction
        if self.backflipping:
            self.animBackflip.play()



    def whipattack(self):
        """
    fait attaquer au fouet le joueur
    est lancée si l'on appuye sur B en etant au sol debout, accroupi ou en l'air
        """
        self.whipping = True
        self.whipped = True
        if not self.onGround:
            self.jumpwhipping = True
            self.image = self.animWhipJump
            if self.animWhipJump.isFinished():
                self.animWhipJump.stop()
                self.image = richtersheet.image_at((202,410,16,32), alpha)
                self.whipping = False
                self.jumpwhipping = False
            if self.whipping:
                self.animWhipJump.play()
            # si le joueur est en l'air
            # l'image joueur devient l'animation de fouet en l'air
            # arreter de lire la fonction lorsque l'animation est finie
        if self.onGround and not self.crouching:
            self.xvel = 0
            self.image = self.animWhipGround
            if self.jumpwhipping:
                self.animWhipGround.play()
                self.animWhipGround.elapsed = self.animWhipJump.elapsed
                self.animWhipJump.stop()
                self.jumpwhipping = False
                # s'il atterrit d'un saut, continuer et finir avec l'animation au sol
            if self.animWhipGround.isFinished():
                self.whipping = False
                self.animWhipGround.stop()
                self.image = richtersheet.image_at((202,206,16,32), alpha)
            if self.whipping:
                self.animWhipGround.play()
            # si le joueur est au sol debout
            # il ne peut pas bouger a droite ou a gauche
            # l'image joueur devient l'animation de fouet accroupi
            # arreter de lire la fonction lorsque l'animation est finie
        if self.crouching:
            self.image = self.animWhipCrouch
            if self.animWhipCrouch.isFinished():
                self.whipping = False
                self.animWhipCrouch.stop()
                self.image = richtersheet.image_at((202,308,16,32), alpha)
            if self.whipping:
                self.animWhipCrouch.play()
            # si le joueur est accroupi
            # l'image joueur devient l'animation de fouet accroupi
            # arreter de lire la fonction lorsque l'animation est finie


    def useitem(self):
        """
    fait utiliser un hache au joueur
    est lancée si l'on appuye sur haut et B en meme temps
        """
        if not self.useditem and self.axelist != [1, 1]:
            self.ammo -= 1
            if self.axelist == [1, 0]:
                self.axelist = [1, 1]
            if self.axelist == [0, 0]:
                self.axelist = [1, 0]
        # si cette fonction est lue pour la premiere fois
        # diminuer de 1 les munitions du joueur
        # changer axelist comme il se doit (chaque element est une instance de hache)
        self.usingitem = True
        self.useditem = True
        if not self.onGround:
            self.jumpusingitem = True
            self.image = self.animItemJump
            if self.animItemJump.isFinished():
                self.usingitem = False
                self.animItemJump.stop()
                self.jumpusingitem = False
            if self.usingitem:
                self.animItemJump.play()
        if self.onGround:
            self.xvel = 0
            self.image = self.animItemGround
            if self.jumpusingitem:
                self.animItemGround.play()
                self.animItemGround.elapsed = self.animItemJump.elapsed
                self.animItemJump.stop()
                self.jumpusingitem = False
            if self.animItemGround.isFinished():
                self.usingitem = False
                self.animItemGround.stop()
            if self.usingitem:
                self.animItemGround.play()
        # cette fonction est analogue a whipattack()
        # les commentaires qui y sont expliquent aussi bien celle-ci


    def slide(self):
        """
    fait faire au joueur une glissade au sol
    est lancée si A est enfoncé lorsque le joueur est accroupi
        """
        self.sliding = True
        self.slided = True
        self.image = self.animSlide
        if self.facingRight:
            self.xvel = 4
            if self.animSlide.elapsed > 0.4:
                self.xvel = 2
        if not self.facingRight:
            self.xvel = -4
            if self.animSlide.elapsed > 0.4:
                self.xvel = -2
            # faire glisser le joueur a 4 pixels/frame, puis a 2 pixels/frame
        if self.animSlide.isFinished():
            self.sliding = False
            self.animSlide.stop()
            self.image = richtersheet.image_at((20,70,16,32), alpha)
        if self.sliding:
            self.animSlide.play()


    def slidekick(self):
        """
    fait faire un coup de pied glissade aerien au joueur
    est lancée si A est enfoncé lorsque le joueur est en train glisser au sol
        """
        self.sliding = False
        self.animSlide.stop()
        if not self.slidekicking:
            self.yvel = -6
        self.slidekicking = True
        self.slidekicked = True
        self.onGround = False
        self.image = self.animSlidekick
        if self.animSlidekick.elapsed <= 0.5:
            self.xvel = 6
        elif self.animSlidekick.elapsed <= 0.8:
            self.xvel = 5
        elif self.animSlidekick.elapsed <= 0.9:
            self.xvel = 3
        elif self.animSlidekick.elapsed <= 1:
            self.xvel = 1
            # incrementer la vitesse au cours du mouvement
        if not self.facingRight and self.xvel > 0:
            self.xvel = self.xvel*(-1)
            # si le joueur va vers la droite, faire la meme chose mais *(-1)
        if self.animSlidekick.isFinished():
            self.slidekicking = False
            self.animSlidekick.stop()
            if self.facingRight:
                self.facingRight = False
            elif not self.facingRight:
                self.facingRight = True
                # changer la direction vers laquelle regarde le joueur
            self.onGround = True
            self.crouching = True
            self.image = richtersheet.image_at((2,70,16,32), alpha)
        if self.slidekicking:
            self.animSlidekick.play()

    
    def takedamage(self, damage=0):
        """
    fait sauter en arriere et prendre des degats au joueur
    est lancée s'il y a collision entre le joueur et un ennemi
        """
        if not self.takingDamage:
            self.yvel = -4
            self.onGround = False
            self.health -= damage
            # si cette fonction est lue pour la 1ere fois
            # soustraire des points de vie au joueur et le faire sauter
        if self.facingRight:
            self.xvel = -3
        if not self.facingRight:
            self.xvel = 3
            # faire bouger en arriere a 2 pixels/frame
        self.takingDamage = True
        self.invulnerable = True
        if self.onGround:
            self.takingDamage = False
        if self.yvel > 0:
            self.image = richtersheet.image_at((2,614,16,32), alpha)
        if self.yvel <= 0:
            self.image = richtersheet.image_at((20,614,24,24), alpha)
            # l'image est reglée en fonction d'ou il est en est de son saut

#   ================ Definition du sprite des attaques =================

    class Attack(Sprite):
        """
    sous-classe qui gere les animations et collisions pour les attaques (hors haches)
        """
        def __init__(self, x, y):
            Sprite.__init__(self)
            
            self.xcoord = x
            self.ycoord = y
            # coordonnees du sprite attack
            
            self.animWhip = pyganim.PygAnimation([
                (richtersheet.image_at((2,206,16,24), alpha), 0.1),
                (richtersheet.image_at((36,206,24,16), alpha), 0.05),
                (richtersheet.image_at((94,206,40,16), alpha), 0.05),
                (richtersheet.image_at((152,206,48,16), alpha), 0.2),
                (richtersheet.image_at((218,206,16,16), alpha), 0.05)], False)
            self.animWhip.loop = False
            # animation du fouet lorsqu'il attaque
            self.animItem = pyganim.PygAnimation([
                (richtersheet.image_at((2,274,8,16), alpha), 0.1),
                (richtersheet.image_at((28,274,8,8), alpha), 0.05),
                (richtersheet.image_at((62,274,8,16), alpha), 0.05)], False)
            self.animItem.loop = False
            # animation du bras lorsqu'il lance une hache
            self.animSlide = pyganim.PygAnimation([
                (richtersheet.image_at((18,512,8,32), alpha), 0.05),
                (richtersheet.image_at((44,528,16,16), alpha), 0.05),
                (richtersheet.image_at((78,528,16,16), alpha), 0.3),
                (richtersheet.image_at((112,528,16,16), alpha), 0.1)], False)
            self.animSlide.loop = False
            # animation des pieds lorsqu'il glisse
            self.animSlidekick = pyganim.PygAnimation([
                (richtersheet.image_at((18,562,16,16), alpha), 0.1),
                (richtersheet.image_at((52,562,16,16), alpha), 0.4),
                (richtersheet.image_at((86,562,16,16), alpha), 0.1),
                (richtersheet.image_at((120,562,16,16), alpha), 0.1),
                (richtersheet.image_at((154,546,8,32), alpha), 0.1)], False)
            self.animSlidekick.loop = False
            # animation des pieds lors d'un coup de pied aerien du joueur
            
            self.rect = pygame.Rect(x, y, 8, 8)
            # le rectangle d'occupation du sprite attack
            self.hitbox = pygame.Rect(x+8, y+16, 1, 1)
            # la hitbox des attaques, differente du rect, qui va gerer les collisions avec les ennemis
            
            self.active = False
            # si attack est censé etre à l'ecran
            
            self.image = pygame.Surface((16, 16))
            # image representant le fouet a tout moment, d'abord un carré transparent de 8x8

#   =================== Mise a jour du sprite attack ===================

        def update(self,
                   player_crouching,
                   player_whipping,
                   player_usingitem,
                   player_sliding,
                   player_slidekicking,
                   player_facingRight,
                   elapsed,
                   player_xcoord, player_ycoord,
                   enemies):


            if not self.active:
                self.rect = pygame.Rect(player_xcoord, player_ycoord, 8, 8)
                self.hitbox = pygame.Rect(player_xcoord+8, player_ycoord+16, 1, 1)
                self.image = pygame.Surface((16, 16))

            if player_whipping:
                self.whip(player_crouching, player_facingRight, elapsed, player_xcoord, player_ycoord)

            if player_usingitem:
                self.useitem(player_facingRight, elapsed, player_xcoord, player_ycoord)

            if player_sliding:
                self.slide(player_facingRight, elapsed, player_xcoord, player_ycoord)

            if player_slidekicking:
                self.slidekick(player_facingRight, elapsed, player_xcoord, player_ycoord)
                
            if (not player_whipping
            and not player_usingitem
            and not player_sliding
            and not player_slidekicking):
                self.active = False

#   =================== Reglage de l'image attack ======================

            if isinstance(self.image, pyganim.PygAnimation):
                self.image = self.image.getCurrentFrame()
            if not player_facingRight:
                self.image = transform.flip(self.image, True, False)
        # ces lignes sont identiques a celles dans la fonction update() du joueur
        # les commentaires qui y sont expliquent aussi bien ceci

#   =============== Deplacement du sprite et collisions ================

            self.xcoord = self.rect.topleft[0]
            self.ycoord = self.rect.topleft[1]
            # incrementer la position du rect

            if self.active:
                self.collide(enemies)
            # faire les collisions

#   ===================== Fonctions d'actions attack ===================

        def collide(self, enemies):
            """
        fonction pour verifier le collisions des attaques du joueur avec les ennemis
            """
            for n in enemies:  
                if self.hitbox.colliderect(n.rect):
                    if isinstance(n, BonePillar) and not n.invulnerable:
                        n.takedamage(1)


        def whip(self, player_crouching, player_facingRight, elapsed, player_xcoord, player_ycoord):
            """
        gere le fouet lorsque le joueur attaque au fouet
        est lancée si le joueur fouette
            """
            self.active = True
            self.image = self.animWhip
            self.animWhip.play()
            if player_crouching:
                if player_facingRight:
                    if elapsed < 0.1:
                        self.rect = pygame.Rect(player_xcoord-16, player_ycoord+8, 16, 24)
                        self.hitbox = pygame.Rect(player_xcoord-16, player_ycoord+16, 16, 16)
                    elif elapsed < 0.15:
                        self.rect = pygame.Rect(player_xcoord-24, player_ycoord+8, 24, 16)
                        self.hitbox = pygame.Rect(player_xcoord-24, player_ycoord+16, 24, 16)
                    elif elapsed < 0.2:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord+8, 40, 16)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+8, 32, 16)
                    elif elapsed < 0.4:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord+8, 48, 16)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+16, 48, 8)
                    elif elapsed < 0.45:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord+8, 16, 16)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+16, 16, 8)
                    else:
                        self.active = False
                        self.animWhip.stop()
                if not player_facingRight:
                    if elapsed < 0.1:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord+8, 16, 24)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+16, 16, 16)
                    elif elapsed < 0.15:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord+8, 24, 16)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+8, 24, 16)
                    elif elapsed < 0.2:
                        self.rect = pygame.Rect(player_xcoord-40, player_ycoord+8, 40, 16)
                        self.hitbox = pygame.Rect(player_xcoord-40, player_ycoord+8, 32, 16)
                    elif elapsed < 0.4:
                        self.rect = pygame.Rect(player_xcoord-48, player_ycoord+8, 48, 16)
                        self.hitbox = pygame.Rect(player_xcoord-48, player_ycoord+16, 48, 8)
                    elif elapsed < 0.45:
                        self.rect = pygame.Rect(player_xcoord-16, player_ycoord+8, 16, 16)
                        self.hitbox = pygame.Rect(player_xcoord-16, player_ycoord+16, 16, 8)
                    else:
                        self.active = False
                        self.animWhip.stop()
                    # placer correctement la hitbox et le rect des attaques a chaque frame
                    # et arreter quand l'animation est finie

            else:
                if player_facingRight:
                    if elapsed < 0.1:
                        self.rect = pygame.Rect(player_xcoord-16, player_ycoord, 16, 24)
                        self.hitbox = pygame.Rect(player_xcoord-16, player_ycoord+8, 16, 16)
                    elif elapsed < 0.15:
                        self.rect = pygame.Rect(player_xcoord-24, player_ycoord, 24, 16)
                        self.hitbox = pygame.Rect(player_xcoord-24, player_ycoord, 24, 16)
                    elif elapsed < 0.2:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 40, 16)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord, 32, 16)
                    elif elapsed < 0.4:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 48, 16)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+8, 48, 8)
                    elif elapsed < 0.45:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 16, 16)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+8, 16, 8)
                    else:
                        self.active = False
                        self.animWhip.stop()
                if not player_facingRight:
                    if elapsed < 0.1:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 16, 24)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+8, 16, 16)
                    elif elapsed < 0.15:
                        self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 24, 16)
                        self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord, 24, 16)
                    elif elapsed < 0.2:
                        self.rect = pygame.Rect(player_xcoord-40, player_ycoord, 40, 16)
                        self.hitbox = pygame.Rect(player_xcoord-40, player_ycoord, 32, 16)
                    elif elapsed < 0.4:
                        self.rect = pygame.Rect(player_xcoord-48, player_ycoord, 48, 16)
                        self.hitbox = pygame.Rect(player_xcoord-48, player_ycoord+8, 48, 8)
                    elif elapsed < 0.45:
                        self.rect = pygame.Rect(player_xcoord-16, player_ycoord, 16, 16)
                        self.hitbox = pygame.Rect(player_xcoord-16, player_ycoord+8, 16, 8)
                    else:
                        self.active = False
                        self.animWhip.stop()
                    # placer correctement la hitbox et le rect des attaques a chaque frame
                    # et arreter quand l'animation est finie


        def useitem(self, player_facingRight, elapsed, player_xcoord, player_ycoord):
            """
        gere le bras lorsque le joueur lance une hache
        est lancée si le joueur utilise une hache
            """
            self.active = True
            self.image = self.animItem
            self.animItem.play()
            if player_facingRight:
                if elapsed < 0.1:
                    self.rect = pygame.Rect(player_xcoord-8, player_ycoord, 8, 16)
                    self.hitbox = pygame.Rect(player_xcoord-8, player_ycoord+8, 8, 8)
                elif elapsed < 0.15:
                    self.rect = pygame.Rect(player_xcoord, player_ycoord, 8, 8)
                    self.hitbox = pygame.Rect(player_xcoord, player_ycoord, 8, 8)
                elif elapsed < 0.2:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 8, 16)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+8, 8, 8)
                else:
                    self.active = False
                    self.animItem.stop()
            if not player_facingRight:
                if elapsed < 0.1:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 8, 16)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+8, 8, 8)
                elif elapsed < 0.15:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 8, 8)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord, 8, 8)
                elif elapsed < 0.2:
                    self.rect = pygame.Rect(player_xcoord-8, player_ycoord, 8, 16)
                    self.hitbox = pygame.Rect(player_xcoord-8, player_ycoord+8, 8, 8)
                else:
                    self.active = False
                    self.animItem.stop()
                # placer correctement la hitbox et le rect des attaques a chaque frame
                # et arreter quand l'animation est finie


        def slide(self, player_facingRight, elapsed, player_xcoord, player_ycoord):
            """
        gere les attaques des pieds lorsque le joueur fait un slide
        est lancée si le joueur fait un slide
            """
            self.active = True
            self.image = self.animSlide
            self.animSlide.play()
            if player_facingRight:
                if elapsed < 0.05:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 8, 32)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+16, 8, 16)
                elif elapsed < 0.1:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord+16, 16, 16)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+24, 16, 8)
                elif elapsed < 0.4:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord+16, 16, 16)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+16, 16, 16)
                elif elapsed < 0.5:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord+16, 16, 16)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+24, 16, 8)
                else:
                    self.active = False
                    self.animSlide.stop()
            if not player_facingRight:
                if elapsed < 0.05:
                    self.rect = pygame.Rect(player_xcoord-8, player_ycoord, 8, 32)
                    self.hitbox = pygame.Rect(player_xcoord-8, player_ycoord+16, 8, 16)
                elif elapsed < 0.1:
                    self.rect = pygame.Rect(player_xcoord-16, player_ycoord+16, 16, 16)
                    self.hitbox = pygame.Rect(player_xcoord-16, player_ycoord+24, 16, 8)
                elif elapsed < 0.4:
                    self.rect = pygame.Rect(player_xcoord-16, player_ycoord+16, 16, 16)
                    self.hitbox = pygame.Rect(player_xcoord-16, player_ycoord+16, 16, 16)
                elif elapsed < 0.5:
                    self.rect = pygame.Rect(player_xcoord-16, player_ycoord+16, 16, 16)
                    self.hitbox = pygame.Rect(player_xcoord-16, player_ycoord+24, 16, 8)
                else:
                    self.active = False
                    self.animSlide.stop()
                # placer correctement la hitbox et le rect des attaques a chaque frame
                # et arreter quand l'animation est finie


        def slidekick(self, player_facingRight, elapsed, player_xcoord, player_ycoord):
            """
        gere les attaques des pieds lorsque le joueur fait un slidekick
        est lancée si le joueur fait un slidekick
            """
            self.active = True
            self.image = self.animSlidekick
            self.animSlidekick.play()
            if player_facingRight:
                if elapsed < 0.7:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord+16, 16, 16)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+16, 16, 16)
                elif elapsed < 0.8:
                    self.rect = pygame.Rect(player_xcoord+16, player_ycoord, 8, 32)
                    self.hitbox = pygame.Rect(player_xcoord+16, player_ycoord+8, 8, 16)
                else:
                    self.active = False
                    self.animSlidekick.stop()
            if not player_facingRight:
                if elapsed < 0.7:
                    self.rect = pygame.Rect(player_xcoord-16, player_ycoord+16, 16, 16)
                    self.hitbox = pygame.Rect(player_xcoord-16, player_ycoord+16, 16, 16)
                elif elapsed < 0.8:
                    self.rect = pygame.Rect(player_xcoord-8, player_ycoord, 8, 32)
                    self.hitbox = pygame.Rect(player_xcoord-8, player_ycoord+8, 8, 16)
                else:
                    self.active = False
                    self.animSlidekick.stop()
                # placer correctement la hitbox et le rect des attaques a chaque frame
                # et arreter quand l'animation est finie

#   ================= Definition du sprite des haches ==================

    class ItemAxe(Sprite):
        """
    classe qui gere le mouvement, les animations et collisions pour l'item hache
        """
        def __init__(self, x, y):
            Sprite.__init__(self)

            self.xcoord = x
            self.ycoord = y
            # coordonnees du sprite

            self.xvel = 0
            self.yvel = 0
            # vitesse horizontale et verticale du sprite

            self.animSpin = pyganim.PygAnimation([
                (axesheet.image_at((280,0,16,16), alpha), 0.1),
                (axesheet.image_at((296,0,16,16), alpha), 0.1),
                (axesheet.image_at((312,0,16,16), alpha), 0.1),
                (axesheet.image_at((328,0,16,16), alpha), 0.1)])
            self.animSpin.loop = True
            # animation de la hache tournante

            self.rect = pygame.Rect(x, y, 16, 16)
            # le rectangle d'occupation du sprite

            self.active = False
            # si la hache est a l'ecran

            self.throwDelay = 0
            # permet de lancer la hache avec un peu de retard par rapport au mouvement du joueur

            self.image = pygame.Surface((16, 16))
            # image, d'abord affectée a une Surface vide

#   =================== Mise a jour du sprite hache ====================

        def update(self, elapsed, player_facingRight,
                   player_usingitem, player_useditem,
                   player_xcoord, player_ycoord,
                   enemies):

            if not self.active:
                if player_facingRight:
                    self.rect = pygame.Rect(player_xcoord-8, player_ycoord+16, 16, 16)
                if not player_facingRight:
                    self.rect = pygame.Rect(player_xcoord+8, player_ycoord+16, 16, 16)
                self.image = pygame.Surface((16, 16))

            if self.ycoord > 224 and not player_usingitem:
                self.throwDelay = 0
                self.animSpin.stop()
                self.active = False

            if player_usingitem:
                if not self.active:
                    self.yvel = -9
                    if player_facingRight:
                        self.xvel = 3
                    if not player_facingRight:
                        self.xvel = -3
                self.active = True

            if self.active:
                self.yvel += 0.5
                self.yvel = min(25, self.yvel)
                self.image = self.animSpin
                self.animSpin.play()

#   =================== Reglage de l'image attack ======================
        
            if isinstance(self.image, pyganim.PygAnimation):
                self.image = self.image.getCurrentFrame()

            if self.xvel < 0:
                self.image = transform.flip(self.image, True, False)
            # ces lignes sont identiques a celles dans la fonction update() du joueur
            # les commentaires qui y sont expliquent aussi bien ceci

#   =============== Deplacement du sprite et collisions ================

            self.rect.x += self.xvel
            self.rect.y += self.yvel
            # faire bouger le rect hache
                
            self.xcoord = self.rect.topleft[0]
            self.ycoord = self.rect.topleft[1]
            # mettre a jour les valeurs de xcoord et ycoord
            
            if self.active:
                for n in enemies:  
                    if pygame.sprite.collide_rect(self, n):
                        if isinstance(n, BonePillar) and not n.invulnerable:
                            n.takedamage(1)
                # faire les collisions