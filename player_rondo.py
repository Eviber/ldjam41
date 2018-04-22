from balls import *
from pyganim import *



alpha = (185,209,217)



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tigersheet):
        pygame.sprite.Sprite.__init__(self)
        self.tigersheet = tigersheet

        self.attack = self.Attack(x, y, self)
        self.bomb = self.ItemBomb(x, y)


        self.pos_x = x
        self.pos_y = y

        self.vel_x = 0
        self.vel_y = 0

        self.facingRight = True
        self.onGround = True
        self.invulnerable = False

        self.takingDamage = False
        self.idling = True
        self.walking = False
        self.crouching = False
        self.jumping = False
        #self.hitting = False  #Todo ?
        self.swinging = False
        self.usingitem = False
        self.jumpswinging = False
        self.jumpusingitem = False

        self.jumped = False
        self.swung = False
        self.useditem = False
        #prevents continuous input of moves

        #TODO fix values @lexou
        self.image = tigersheet.image_at((2,2,16,32), alpha)
        #self.image = tigersheet.
        self.elapsed = None
        # point at which the current animation is, specified in seconds

        self.rect = pygame.Rect(x, y, 64, 64)
        # collision rectangle
        self.hitbox = pygame.Rect(x+2, y+2, 12, 30)
        # hitbox rect < coll rect


        self.health = 3
        self.healthList = [1,1,1]

        self.score = 0 #TODO make list of the score tuple for each hole/level
        self.corefind_time = 0
        self.return_time = 0
        self.core_swings = 0
        self.coreswing_count = "0"
        #Todo other ?

        self.max_ammo = 5
        self.ammo = 5
        #bomb ammo
        
#   =============== Definition des animations du joueur ================
        
# a l'aide du module PygAnim
		
        self.animWalk = PygAnimation([
            (tigersheet.image_at((2, 138, 16, 32), alpha), 0.2),
            (tigersheet.image_at((20, 138, 16, 32), alpha), 0.2),
            (tigersheet.image_at((38, 138, 16, 32), alpha), 0.2),
            (tigersheet.image_at((56, 138, 16, 32), alpha), 0.2)])
        
        self.animSwingGround = PygAnimation([
            (tigersheet.image_at((18, 206, 16, 32), alpha), 0.1),
            (tigersheet.image_at((60, 206, 16, 32), alpha), 0.05),
            (tigersheet.image_at((78, 206, 16, 32), alpha), 0.05),
            (tigersheet.image_at((136, 206, 16, 32), alpha), 0.2),
            (tigersheet.image_at((202, 206, 16, 32), alpha), 0.05)], False)
        self.animSwingGround.loop = False

        self.animSwingCrouch = PygAnimation([
            (tigersheet.image_at((18, 308, 16, 32), alpha), 0.1),
            (tigersheet.image_at((60, 308, 16, 32), alpha), 0.05),
            (tigersheet.image_at((78, 308, 16, 32), alpha), 0.05),
            (tigersheet.image_at((136, 308, 16, 32), alpha), 0.2),
            (tigersheet.image_at((202, 308, 16, 32), alpha), 0.05)], False)
        self.animSwingCrouch.loop = False
        # animation d'attaque fouet du joueur accroupi
        self.animSwingJump = PygAnimation([
            (tigersheet.image_at((18, 410, 16, 32), alpha), 0.1),
            (tigersheet.image_at((60, 410, 16, 32), alpha), 0.05),
            (tigersheet.image_at((78, 410, 16, 32), alpha), 0.05),
            (tigersheet.image_at((136, 410, 16, 32), alpha), 0.2),
            (tigersheet.image_at((202, 410, 16, 32), alpha), 0.05)], False)
        self.animSwingJump.loop = False
        # animation d'attaque fouet du joueur en l'air

        self.animItemGround = PygAnimation([
            (tigersheet.image_at((10, 274, 16, 32), alpha), 0.1),
            (tigersheet.image_at((28, 274, 16, 32), alpha), 0.05),
            (tigersheet.image_at((46, 274, 16, 32), alpha), 0.05),
            (tigersheet.image_at((72, 274, 16, 32), alpha), 0.15)], False)
        self.animItemGround.loop = False

        self.animItemJump = PygAnimation([
            (tigersheet.image_at((10, 444, 16, 32), alpha), 0.1),
            (tigersheet.image_at((28, 444, 16, 32), alpha), 0.05),
            (tigersheet.image_at((46, 444, 16, 32), alpha), 0.05),
            (tigersheet.image_at((72, 444, 16, 32), alpha), 0.15)], False)
        self.animItemJump.loop = False


	
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
               
        self.elapsed = None
        
#   ======================= Conditions ========================

        if not self.onGround:
            self.fall()
            
        if up or down or left or right or Abutton or Bbutton or Lbutton or Rbutton:
            self.idling = False
        
        if not down:
            self.crouching = False

        #already acting
        if not (self.swinging or
                self.usingitem or
                self.takingDamage):

            if (left or right):
                self.walk(left, right)
            if (releaseLeft or releaseRight):
                self.walking = False

            if Abutton:
                self.jump()

            if Lbutton and not self.useditem and self.ammo > 0 and not self.bomb.active:
                self.useitem()



            if not self.onGround:
                if Bbutton and not self.swung and not self.usingitem:
                    self.swing()


            if self.onGround:
                if not(up or down or left or right or Abutton or Bbutton):
                    self.idle()
                if Bbutton and not self.swung and not self.usingitem:
                    self.jumpswing()
                if down:
                    self.crouch()


        if not Abutton and self.onGround:
            self.jumped = False
        if not Bbutton and not self.swinging:
            self.swung = False
        if not Bbutton and not self.usingitem and not self.bomb.active:
            self.useditem = False

        if self.usingitem:
            self.useitem()
        if self.takingDamage:
            self.takedamage()

#   =============== Movement & collisions ================

        self.rect.x += self.vel_x
        self.pos_x = self.rect.x
        self.collidewall(self.vel_x, 0, platforms)

        self.rect.y += self.vel_y
        self.pos_y = self.rect.y
        self.collidewall(0, self.vel_y, platforms)

        self.collideenemy(enemies)

#   ================ Hitbox ====================

        if (self.takingDamage or
            self.idling or
            self.walking or
            self.jumping or
            self.swinging or
            self.jumpswinging or
            self.usingitem or
            self.jumpusingitem):
            self.hitbox = pygame.Rect(self.pos_x + 2, self.pos_y + 2, 12, 30) #TODO FIX
            
        elif (self.crouching):
            self.hitbox = pygame.Rect(self.pos_x + 2, self.pos_y + 16, 12, 16) #TODO FIX


#   =================== Player image ======================

        if isinstance(self.image, PygAnimation):
            self.elapsed = self.image.elapsed
            self.image = self.image.getCurrentFrame()
        if not self.facingRight:
            self.image = transform.flip(self.image, True, False)

#   ================== Value boundaries =================

        self.health = max(0, self.health)
        self.health = min(3, self.health)
        #self.score = max(0, self.score)
        #self.score = min(999999, self.score)
        self.ammo = max(0, self.ammo)
        self.ammo = min(self.max_ammo, self.ammo)


#   ================== Subclass updates ====================

        self.attack.update(self.crouching,
                           self.swinging,
                           self.usingitem,
                           self.facingRight,
                           self.elapsed,
                           self.pos_x, self.pos_y,
                           enemies)
        
        if self.bomb.active:
            self.bomb.update(self.elapsed, self.facingRight,
                             self.usingitem, self.useditem,
                             self.pos_x, self.pos_y,
                             enemies)



    def collidewall(self, xvel, yvel, platforms):
        collideUnder = 0
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.jumping = False
                    self.vel_y = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0
            if p.rect.collidepoint(self.rect.left, self.rect.bottom) or p.rect.collidepoint(self.rect.right, self.rect.bottom):
                collideUnder = 1
        if collideUnder == 0:
            self.onGround = False


    def collideenemy(self, enemies):
        for n in enemies:
            if self.hitbox.colliderect(n.rect):
                self.takedamage(1)

    def idle(self):
        self.image = tigersheet.image_at((2, 2, 16, 32), alpha)
        if self.crouching:
            self.image = tigersheet.image_at((2, 70, 16, 32), alpha)
        self.idling = True
        self.crouching = False
        self.vel_x = 0


    def crouch(self):
        if not self.crouching:
            self.image = tigersheet.image_at((2, 70, 16, 32), alpha)
        if self.crouching:
            self.image = tigersheet.image_at((20, 70, 16, 32), alpha)
        self.crouching = True
        self.idling = False
        self.taunting = False
        self.vel_x = 0


    def walk(self, left, right):
        self.walking = True
        if right:
            self.vel_x = 2
            if not self.facingRight:
                self.facingRight = True
            if self.onGround:
                self.image = self.animWalk
                self.animWalk.play()
        if left:
            self.vel_x = -2
            if self.facingRight:
                self.facingRight = False
            if self.onGround:
                self.image = self.animWalk
                self.animWalk.play()


    #TODO add aerial DI ?
    def jump(self):
        if self.onGround and not self.jumped:
            self.vel_y = -5
            self.jumping = True
            self.jumped = True
            self.onGround = False
            self.crouching = False
            self.taunting = False
        if self.jumped and self.vel_y < 0:
            self.vel_y -= 0.2


    def fall(self):
        self.vel_y += 0.5
        if self.vel_y > 25: self.vel_y = 25
        if self.vel_y < 0:
            if self.vel_x == 0:
                self.image = tigersheet.image_at((2, 104, 16, 32), alpha)
            else:
                self.image = tigersheet.image_at((20, 104, 16, 32), alpha)
        if 2 >= self.vel_y >= 0:
            self.image = tigersheet.image_at((38, 104, 16, 32), alpha)
        if self.vel_y > 2:
            self.image = tigersheet.image_at((56, 104, 16, 32), alpha)



    def swing(self):
        # TODO implement
        return



    def useitem(self):
        if not self.useditem and not self.bombout:
            self.ammo -= 1
            self.bomb.active = True
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
            self.vel_x = 0
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
    
    def takedamage(self, damage=0):
        if not self.takingDamage:
            self.vel_y = -4
            self.onGround = False
            self.health -= damage
        if self.facingRight:
            self.vel_x = -3
        if not self.facingRight:
            self.vel_x = 3
        self.takingDamage = True
        self.invulnerable = True
        if self.onGround:
            self.takingDamage = False
        if self.vel_y > 0:
            self.image = tigersheet.image_at((2, 614, 16, 32), alpha)
        if self.vel_y <= 0:
            self.image = tigersheet.image_at((20, 614, 24, 24), alpha)




#   ================ Attack sprite subclass =================

    class Attack(pygame.sprite.Sprite):
        def __init__(self, x, y, player):
            pygame.sprite.Sprite.__init__(self)
            
            self.xcoord = x
            self.ycoord = y
            self.player = player
            
            self.animSwing = PygAnimation([
                (player.tigersheet.image_at((2, 206, 16, 24), alpha), 0.1),
                (player.tigersheet.image_at((36, 206, 24, 16), alpha), 0.05),
                (player.tigersheet.image_at((94, 206, 40, 16), alpha), 0.05),
                (player.tigersheet.image_at((152, 206, 48, 16), alpha), 0.2),
                (player.tigersheet.image_at((218, 206, 16, 16), alpha), 0.05)], False)
            self.animSwing.loop = False

            self.animItem = PygAnimation([
                (player.tigersheet.image_at((2, 274, 8, 16), alpha), 0.1),
                (player.tigersheet.image_at((28, 274, 8, 8), alpha), 0.05),
                (player.tigersheet.image_at((62, 274, 8, 16), alpha), 0.05)], False)
            self.animItem.loop = False

            self.rect = pygame.Rect(x, y, 8, 8)
            # attack sprite rectangle
            self.hitbox = pygame.Rect(x+8, y+16, 1, 1)
            # hitbox rectangle
            
            self.active = False
            
            self.image = pygame.Surface((16, 16)) #TODO fix ?
            # image for the club

        def update(self,
                   player_crouching,
                   player_swinging,
                   player_usingitem,
                   player_facingRight,
                   elapsed,
                   player_xcoord, player_ycoord,
                   enemies):


            if not self.active:
                self.rect = pygame.Rect(player_xcoord, player_ycoord, 8, 8)
                self.hitbox = pygame.Rect(player_xcoord+8, player_ycoord+16, 1, 1)
                self.image = pygame.Surface((16, 16))

            if player_swinging:
                self.swing(player_crouching, player_facingRight, elapsed, player_xcoord, player_ycoord)

            if player_usingitem:
                self.useitem(player_facingRight, elapsed, player_xcoord, player_ycoord)
                
            if (not player_swinging and not player_usingitem):
                self.active = False

#   =================== Update Attack Image ======================

            if isinstance(self.image, PygAnimation):
                self.image = self.image.getCurrentFrame()
            if not player_facingRight:
                self.image = transform.flip(self.image, True, False)

#   =============== Movement and collision ================

            self.xcoord = self.rect.topleft[0]
            self.ycoord = self.rect.topleft[1]

            if self.active:
                self.collide(enemies)

#   ===================== Fonctions d'actions attack ===================

        def collide(self, enemies):
            for n in enemies:  
                if self.hitbox.colliderect(n.rect):
                    if isinstance(n, BonePillar) and not n.invulnerable:
                        n.takedamage(1)


        def swing(self, player_crouching, player_facingRight, elapsed, player_xcoord, player_ycoord):
            self.active = True
            self.image = self.animSwing
            self.animSwing.play()
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
                        self.animSwing.stop()
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
                        self.animSwing.stop()

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
                        self.animSwing.stop()
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
                        self.animSwing.stop()
                    # placer correctement la hitbox et le rect des attaques a chaque frame
                    # et arreter quand l'animation est finie



#   ================= Makes a bomb into a spawnable item ==================

    class ItemBomb(Bomb):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)


            # vitesse horizontale et verticale du sprite

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
        
            if isinstance(self.image, PygAnimation):
                self.image = self.image.getCurrentFrame()

            if self.xvel < 0:
                self.image = transform.flip(self.image, True, False)

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