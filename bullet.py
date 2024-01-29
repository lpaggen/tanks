import pygame
from settings import *
import math
from obstacle import Obstacle

# bullet class
class Bullet(pygame.sprite.Sprite): # should update to differentiate between player and ai
    bulletInstances = []
    bullet_group = pygame.sprite.Group()
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("player/bulletsprite/bullet_1.bmp").convert_alpha(), 0, player_bullet_size)
        self.image_base = self.image
        self.x = x
        self.y = y
        self.pos = pygame.math.Vector2(x, y)
        self.hitbox_rect = self.image_base.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.mask = pygame.mask.from_surface(self.image_base)
        self.velocity = player_bullet_velocity
        self.angle = math.radians(angle)
        self.dead = False # indicator to check if the bullets are dead or not

        Bullet.bulletInstances.append(self)
        Bullet.bullet_group.add(self)

    def move_bullet(self):
        self.vel_x = self.velocity * math.cos(self.angle)
        self.vel_y = self.velocity * math.sin(self.angle)
        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.pos

    def bullet_collide(self):
        other_bullets = [instance for instance in Bullet.bulletInstances if instance.pos != self.pos and not instance.dead] # all bullets except self
        for instance in other_bullets:
            if self.hitbox_rect.colliderect(instance.hitbox_rect): # checks coll with bullets
                self.kill()
                instance.kill()

        for obstacle in Obstacle.obstaclesInstances:
            if self.hitbox_rect.colliderect(obstacle.hitbox_rect):
                self.kill()

    def update(self):
        self.move_bullet()
        self.bullet_collide()