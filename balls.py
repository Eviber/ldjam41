class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rotations = build_rotations(self.image)
        self.diameter = self.image.width
        #index 0 is the default sprite orientation

    def update(self):


class Bomb(Ball):
