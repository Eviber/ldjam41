# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 13:54:39 2013

@author: Alexis Duquesne & Romain Alvarez
"""
# merci au blogger nandnor.net, dont le jeu de plateforme a été une grande aide
# aller voir sur http://www.nandnor.net/?p=64

# pour jouer, il s'agit de battre le dragon qui s'en prend a vous
# se deplacer : touches fleches
# sauter : espace
# attaquer : alt
# esquiver : ctrl gauche
# essayez des combinaisons de touches !

#   ============== Importation des librairies et modules ===============
import pygame
from pygame import *
# librairie permettant l'ouverture d'une fenetre, affichage des sprites, etc
import spritesheet
# module permettant de charger une image en rectangle depuis un fichier bitmap

#   ========= Initialisation/Definition des variables globales =========

levelWidth  = 512
levelHeight = 224
# largeur et longueur du niveau
windowWidth = 256
windowHeight = 224
# largeur et longueur de la fenetre de jeu

pygame.init()
# initialiser la librairie pygame

screen = pygame.display.set_mode((windowWidth, windowHeight), 0, 16)
# screen est la fenetre qu'ouvre le programme pour y afficher le jeu
pygame.display.set_caption("Projet ISN")
# faire que la barre titre de la fenetre affiche "Projet ISN"
timer = pygame.time.Clock()
# timer est assigné a une fonction de pygame qui permet de compter dans le temps les frames du jeu

#   ================ Importation des fichiers analogues ================

from player import *
# fichier contenant la definition du sprite joueur, instancié ici
from enemies import *
# fichier contenant la definition du sprite dragon (et quelques autres ennemis), instancié ici

#   ================== Definition de quelques classes ==================

class Sprite(pygame.sprite.Sprite):
    """
permet de donner facilement des attributs qu'auront toutes les classes par heritage, dont notamment:
- self.rect, un tuple de la forme (coordonnée x, coordonnée y, longueur x, longueur y)
- self.image, un objet "pygame.Surface" qui dessine des pixels a l'ecran
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Platform(Sprite):
    """
sprite des plateformes solides, de taille 16x16
    """
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.Surface((16, 16))
        self.rect = pygame.Rect(x, y, 16, 16)


class Camera(object):
    """
classe qui gere l'affichage du niveau du jeu sur l'ecran qui est plus petit
    """
    def __init__(self, width, height):
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.playerCamera(self.state, target.rect)
        
    def playerCamera(self, level, target_rect):
        xcoord = target_rect[0]
        ycoord = target_rect[1]
        xlength = level[2]
        ylength = level[3]
        xcoord = -xcoord + (windowWidth/2)
        ycoord = -ycoord + (windowHeight/2)
        
        if xcoord > -16:
            xcoord = -16
        if xcoord < -(level.width-windowWidth)+16:
            xcoord = -(level.width-windowWidth)+16
        if ycoord > 0:
            ycoord = 0
        if ycoord < -(level.height-windowHeight):
            ycoord = -(level.height-windowHeight)
    
        return pygame.Rect(xcoord, ycoord, xlength, ylength)

#   =================== Fonction principale du jeu =====================

def main():

#   ================ Chargement des images a utiliser ==================

    bgsheet = spritesheet.spritesheet("Bridge.png")
    # l'image dont on va tirer le decor et divers autres elements grace au module spritesheet

    hud = bgsheet.image_at((0,0,256,32), colorkey=(185,209,217))
    bg1 = bgsheet.image_at((0,32,352,136))
    bg2 = bgsheet.image_at((0,208,376,65))
    bridge = bgsheet.image_at((0,168,512,40), colorkey=(185,209,217))
    # hud (Heads Up Display) est le menu en haut de l'ecran
    # bg1 (BackGround 1) est l'image des nuages du decor
    # bg2 (BackGround 2) est l'image de l'horizon du decor
    # bridge est l'image du pont sous les pieds du joueur

    HPFullPlayer = bgsheet.image_at((256,0,4,8))
    HPEmptyPlayer = bgsheet.image_at((268,0,4,8))
    HPFullEnemy = bgsheet.image_at((256,8,4,8))
    HPEmptyEnemy = bgsheet.image_at((268,8,4,8))
    # images des unités pleines et vides des barres de vie du joueur et du dragon

    number = [bgsheet.image_at((352,16,8,8)),
              bgsheet.image_at((360,16,8,8)),
              bgsheet.image_at((368,16,8,8)),
              bgsheet.image_at((376,16,8,8)),
              bgsheet.image_at((384,16,8,8)),
              bgsheet.image_at((392,16,8,8)),
              bgsheet.image_at((400,16,8,8)),
              bgsheet.image_at((408,16,8,8)),
              bgsheet.image_at((416,16,8,8)),
              bgsheet.image_at((424,16,8,8))]
    # une liste avec les images de chacun des caracteres de numeros, en ordre 0 à 9

#   ======================= Generation du terrain ======================

    platforms = pygame.sprite.Group()
    # platforms est un groupe contenant toutes les plateformes solides constituant le terrain

    platform_x = 0
    platform_y = 0
    # creer les coordonnées x et y des plateformes, d'abord a 0
    
    level = [
    "P                              P",
    "P                              P",
    "P                              P",
    "P                              P",
    "P                              P",
    "P                              P",
    "P                              P",
    "P                              P",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P                              P",
    "P                              P",
    "P                              P",
    "P                              P"]  
    # construire le terrain solide du niveau avec la liste level
    
    for level_x in level:
        for level_y in level_x:
            if level_y == "P":
                p = Platform(platform_x, platform_y)
                platforms.add(p)
            platform_x += 16
        platform_x = 0
        platform_y += 16
    # boucle qui va remplir la liste platforms de sprites plateformes
        
#   ===================== Generation des sprites =======================
        
    entities = pygame.sprite.Group()
    # entities est un groupe contenant tous les sprites du jeu
    enemies = pygame.sprite.Group()
    # enemies est un groupe contenant tous les sprites pouvant infliger des degats au joueur

    camera = Camera(levelWidth, levelHeight)
    # creer l'instance de l'objet camera

    player = Player(16, 128)
    # creer l'instance du sprite joueur, les parametres definissent son lieu d'apparition (x,y)
    entities.add(player)
    # ajouter l'instance player et fouet a la liste entities

    bonepillar = BonePillar(200, 112, False, 0)
    entities.add(bonepillar)
    enemies.add(bonepillar)

#   =================== Creation d'autres variables ====================

    up = releaseUp = False
    down = releaseDown = False
    left = releaseLeft = False
    right = releaseRight = False
    Abutton = releaseAbutton = False
    Bbutton = releaseBbutton = False
    Lbutton = releaseLbutton = False
    Rbutton = releaseRbutton = False
    # on assigne faux a toutes les valeurs des touches enfoncées et relachées (haut, bas gauche, droite, A, B, L et R)
    # ces noms de boutons (ABLR) sont choisis en rapport avec les touches d'une manette classique

    gameTime = 0
    # entier comptant le temps de jeu en frames
    shownTime = "000"
    # chaine de 3 caracteres pour l'affichage à l'ecran du temps de jeu en secondes
    
    myfont = pygame.font.SysFont("monospace", 12)
    # definition d'une police de caractere, pour afficher infoblit
    
#   ===================== Boucle principale du jeu =====================
    
    while True:
    
#   ======================= Mise a jour du temps =======================

        timer.tick(30)
        # regler le nombre de frames par seconde a 30
        gameTime += 1
        # ajouter 1 au comptage de frames
        
        if gameTime%30 == 0:
            shownTime = str(gameTime/30)
            if len(shownTime) == 1:
                shownTime = "00" + shownTime
            if len(shownTime) == 2:
                shownTime = "0" + shownTime
            if len(shownTime) > 3:
                shownTime = "999"
        # si le nombre de frames est un multiple de 30
        # ajouter une seconde a shownTime, en s'assurant qu'il a bien 3 caracteres
        
#   =============== Mise a jour des evenements de touches ==============
        
        prevUp = up
        prevDown = down
        prevLeft = left
        prevRight = right
        prevAbutton = Abutton
        prevBbutton = Bbutton
        prevLbutton = Lbutton
        prevRbutton = Rbutton
        # ces variables correspondent aux touches enfoncees a la frame precedente
        
        for e in pygame.event.get():
        # evenements de touches enfoncées
        
            if e.type == QUIT:
                raise SystemExit("QUIT")
            # si on appuye sur la croix de la fenetre, quitter le programme
            
            if e.type == KEYDOWN and e.key == K_ESCAPE: 
                raise SystemExit("ESCAPE")
            # si on appuye sur echap, quitter le programme
            
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            # assigner vrai a up, down, left et right si les touches fleches correspondantes sont enfoncees
            if e.type == KEYDOWN and e.key == K_SPACE:
                Abutton = True
            if e.type == KEYDOWN and e.key == K_LALT:
                Bbutton = True
            # assigner vrai a A et B si les touches espace et alt respectivement sont enfoncees
            if e.type == KEYDOWN and e.key == K_LCTRL:
                Lbutton = True
            if e.type == KEYDOWN and e.key == K_RCTRL:
                Lbutton = True
            # assigner vrai a L et R si les touches ctrl droite et gauche respectivement sont enfoncees

            if e.type == KEYUP and e.key == K_UP:
                up = False
                if prevUp:  releaseUp = True
                if not prevUp:  releaseUp = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
                if prevDown:  releaseDown = True
                if not prevDown:  releaseDown = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                if prevLeft:  releaseLeft = True
                if not prevLeft:  releaseLeft = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                if prevRight:  releaseRight = True
                if not prevRight:  releaseRight = False
            # assigner faux a up, down, left et right si les touches fleches correspondantes sont relachees
            # si la touche vient d'etre relachée, release__ est mis vrai
            if e.type == KEYUP and e.key == K_SPACE:
                Abutton = False
                if prevAbutton:  releaseAbutton = True
                if not prevAbutton:  releaseAbutton = False
            if e.type == KEYUP and e.key == K_LALT:
                Bbutton = False
                if prevBbutton:  releaseBbutton = True
                if not prevBbutton:  releaseBbutton = False
            # assigner faux a A et B si les touches espace et alt respectivement sont relachees
            # si la touche vient d'etre relachée, release__ est mis vrai
            if e.type == KEYUP and e.key == K_LCTRL:
                Lbutton = False
                if prevLbutton:  releaseLbutton = True
                if not prevLbutton:  releaseLbutton = False
            if e.type == KEYUP and e.key == K_RCTRL:
                Rbutton = False
                if prevRbutton:  releaseRbutton = True
                if not prevRbutton:  releaseRbutton = False
            # assigner faux a L et R si les touches ctrl droite et gauche respectivement sont relachees
            # si la touche vient d'etre relachée, release__ est mis vrai
                
#   ===================== Mise a jour des sprites ======================

        camera.update(player)
        # mettre a jour l'objet camera

        player.update(up, releaseUp,
                      down, releaseDown,
                      left, releaseLeft,
                      right, releaseRight,
                      Abutton, releaseAbutton,
                      Bbutton, releaseBbutton,
                      Lbutton, releaseLbutton,
                      Rbutton, releaseRbutton,
                      platforms, enemies)
        # mettre a jour le sprite joueur

        if not bonepillar.dead:
            bonepillar.update(player.xcoord, player.ycoord)
            
        
                  
        if player.attack.active:
            entities.add(player.attack)
        if not player.attack.active:
            player.attack.kill()
        # si l'image attack n'est pas vide, alors ajouter a entities afin de la dessiner a l'ecran

        if player.axe1.active and player.axelist == [1, 0]:
            entities.add(player.axe1)
        if not player.axe1.active:
            player.axe1.kill()
            player.axelist[0] = 0
        if player.axe2.active and player.axelist == [1, 1]:
            entities.add(player.axe2)
        if not player.axe2.active:
            player.axe2.kill()
            player.axelist[1] = 0
        # si le joueur lance une hache, ajouter celle-ci au groupe entities (2 en meme temps maximum)
        # si les sprites de haches sortent de l'ecran, les enlever du groupe entities



        for b in bonepillar.fireballs:
            if b == 1:
                f = Fireball(bonepillar.xcoord, bonepillar.ycoord, bonepillar.facingRight)
                entities.add(f)

        for f in entities:
            if isinstance(f, Fireball):
                f.update(bonepillar.xcoord,
                         bonepillar.ycoord,
                         bonepillar.attacking,
                         bonepillar.facingRight,
                         bonepillar.idlecount)
                if not  -8 < f.xcoord < 496:
                    del bonepillar.fireballs[1]
                    f.kill()

#   ================== Affichage des images a l'ecran ==================

        screen.blit(bg1, (camera.state[0]/3,
                          camera.state[1]+32,
                          camera.state[2],
                          camera.state[3]))
        # afficher a l'ecran le decor des nuages, defilant 3 fois plus lentement que le terrain

        screen.blit(bg2, (camera.state[0]/2,
                          camera.state[1]+168,
                          camera.state[2],
                          camera.state[3]))
        # afficher a l'ecran le decor de l'horizon, defilant 2 fois plus lentement que le terrain


        for e in entities:
            screen.blit(e.image, camera.apply(e))
        # afficher a l'ecran tous les sprites
            
        screen.blit(bridge, (camera.state[0],
                             camera.state[1]+128,
                             camera.state[2],
                             camera.state[3]))
        # afficher a l'ecran le terrain (le grand pont vert)
                             
        screen.blit(hud, (0,0))
        # afficher a l'ecran le menu en haut de l'ecran, le hud
        
        for n in range(16):
            if player.healthList[n] == 1:
                screen.blit(HPFullPlayer, (4*n+56, 8))
            if player.healthList[n] == 0:
                screen.blit(HPEmptyPlayer, (4*n+56, 8))
            if player.healthList[n] == 1:
                screen.blit(HPFullEnemy, (4*n+56, 16))
            if player.healthList[n] == 0:
                screen.blit(HPEmptyEnemy, (4*n+56, 16))
        # afficher les barres de vie du joueur et du boss

        for n in range(6):
            for i in range(10):
                if player.scoreString[5-n] == str(i):
                    screen.blit(number[i], (88-(8*n), 0))
        # afficher le score du joueur

        for n in range(3):
            for i in range(10):
                if shownTime[2-n] == str(i):
                    screen.blit(number[i], (160-(8*n), 0))
        # afficher le temps de jeu

        if len(str(player.ammo)) == 1:
            screen.blit(number[0], (184, 8))
            screen.blit(number[player.ammo], (192, 8))
        if len(str(player.ammo)) == 2:
            screen.blit(number[int(str(player.ammo)[0])], (184, 8))
            screen.blit(number[int(str(player.ammo)[1])], (192, 8))
        # afficher les munitions d'items du joueur


        infoblit = myfont.render("hp = "+str(bonepillar.health), 1, (0,0,0))
        screen.blit(infoblit, (6, 35))
        # permet de tester, affiche une variable pour voir son etat a tout moment
            
        pygame.display.update()
        # appliquer les affichages dictés à la fenetre

#   ======================== Lancement du jeu ==========================

if(__name__ == "__main__"):
    main()