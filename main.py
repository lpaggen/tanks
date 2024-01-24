import pygame
import math
from random import shuffle, randint
from other_functions import * # useful functions i wrote
import sys

# engine specific modules
from settings import *
from obstacle import *
from bullet import *
from gun import *
from player import *
from powerup import *

# init game
pygame.init()

# create the screen
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# clock
clock = pygame.time.Clock()

# font
font = pygame.font.Font("fonts/PublicPixel-z84yD.ttf", 50)
text_surface = font.render("TANKS", False, "Black")
text_rect = text_surface.get_rect(midbottom = (600, 100))

# background
background = pygame.image.load("graphics/background.bmp").convert_alpha()
background_surface = pygame.transform.scale(background, (width, height))

player = Player(100, 100, health=100, ai = False, idn = 0) # player

# enemy_test = Player(400, 400, health=100, ai = True, idn = 1) # ai instance

obstacle_test = Obstacle(600, 600, 0, 1) # obstacle test
obstacle_test_2 = Obstacle(600, 475, 1, 1)

player_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()

# add player to group
player_group.add(player) # only adds the main body of the player? fix? else blit
gun_group.add(player.gun)
# gun_group.add(enemy_test.gun)
# player_group.add(enemy_test)

# title and icon
pygame.display.set_caption("tanks -- beta")
icon = pygame.image.load("tank1.bmp")
pygame.display.set_icon(icon)

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(background_surface, (0, 0))
    player_group.draw(screen)
    gun_group.draw(screen)
    bullet_group.draw(screen)
    screen.blit(text_surface, text_rect)
    screen.blit(obstacle_test.image, obstacle_test.hitbox_rect)
    screen.blit(obstacle_test_2.image, obstacle_test_2.hitbox_rect)
    player.update()
    # player.raycasting()
    # enemy_test.update()
    bullet_group.update()

    # debug
    pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
    pygame.draw.rect(screen, "yellow", player.rect, width=2)

    # update elements
    pygame.display.update()
    clock.tick(fps)
