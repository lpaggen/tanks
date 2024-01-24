import pygame
from settings import *

# power up class (to do: speed, dmg, health ...)
class powerUps(pygame.sprite.Sprite):
    def __init__(self, x, y, identifier, name, kind, health, points):
        super().__init__()
        self.x = x
        self.y = y
        self.id = identifier
        self.name = name
        self.health = health
        self.points = points
        self.kind = kind

    def set_effect(self, player):
        if self.hitbox_rect.colliderect(player.hitbox_rect):
            if self.kind == 0: # this is a speed boost
                i = 0 # likely need the different variables for the different types of powerups
                while i < 300:
                    player.max_speed = vel_increase # sets top speed higher temporarily
                    i += 1
                player.max_speed = player_max_speed # got this from settings file
            if self.kind == 1: # enables faster shooting speed
                j = 0
                while j < 300:
                    player.shoot_cooldown = shoot_cooldown_decrease # halves the cooldown time needed to do things
                    j += 1
                player.shoot_cooldown = player_shoot_cooldown
            if self.kind == 2:
                if (player_max_health - self.health) < player_max_health / 4: # check if the 25 extra health would surpass player max health
                    player.health = player_max_health # set back to max health
                else:
                    player.health += health_increase # if health is less than 75, add 25 hp
