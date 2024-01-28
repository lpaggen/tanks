import pygame

# gun class (somehow need 2 separate classes for player and guns...)
class Gun(pygame.sprite.Sprite):
    gunInstances = []
    def __init__(self, x, y, size, idn):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.id = idn
        self.gun_pos = pygame.math.Vector2(self.x, self.y)
        self.image = pygame.transform.rotozoom(pygame.image.load(f"player/playersprite/tank_{self.id}_gun.bmp").convert_alpha(), 0, self.size) # gun of the tank
        self.image_base = self.image
        self.hitbox_rect = self.image_base.get_rect(center = self.gun_pos)
        self.rect = self.hitbox_rect.copy()

        Gun.gunInstances.append(self)