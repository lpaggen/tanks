import pygame
import math
from random import shuffle, randint
from other_functions import * # useful functions i wrote
import sys
import json

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
enemy0 = Player(900, 700, 100, ai = True, idn = 1) # Enemy
enemy1 = Player(100, 600, 100, ai = True, idn = 2)

# enemy_test = Player(400, 400, health=100, ai = True, idn = 1) # ai instance

player_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# add player to group
player_group.add(player) # only adds the main body of the player? fix? else blit
gun_group.add(player.gun)
gun_group.add(enemy0.gun)
player_group.add(enemy0)
player_group.add(enemy1)
gun_group.add(enemy1.gun)

# title and icon
pygame.display.set_caption("tanks -- beta")
icon = pygame.image.load("tank1.bmp")
pygame.display.set_icon(icon)

# json file with coordinates of obstacles as saved in the editor.py module
with open("map_data.json", "r") as file:
    map_data = json.load(file)
obs_coords = [(item["x"], item["y"]) for item in map_data]

# create obstacles based on the above coords
i = 0
for coords in obs_coords:
    obs = Obstacle(coords[0], coords[1], i, 0)
    obstacle_group.add(obs)
    i += 1

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # logic for line of sight implementation based on player class and group
    # test for only controlled player LOS first
    players_in_group = []
    id_in_group = []
    for tank in player_group:
        players_in_group.append(tank)
        id_in_group.append(tank.id)
    for key, value in player.visible_players.items(): # player is visible and already in the sprite group
        if value and key in id_in_group:
            continue
        elif value and key not in id_in_group: # player is visible but is not in the sprite group
            player_to_add = Player.playerInstances[key]
            gun_to_add = Gun.gunInstances[key]
            id_in_group.append(key)
            player_group.add(player_to_add)
            gun_group.add(gun_to_add)
        elif not value and key in id_in_group: # player is not visible but is in the sprite group
            player_to_remove = Player.playerInstances[key]
            gun_to_remove = Gun.gunInstances[key]
            id_in_group.remove(key)
            player_group.remove(player_to_remove)
            gun_group.remove(gun_to_remove)
        elif not value and key not in id_in_group: # player not visible and not in sprite group
            continue
    print(id_in_group)

    screen.blit(background_surface, (0, 0))
    player_group.draw(screen)
    gun_group.draw(screen)
    bullet_group.draw(screen)
    obstacle_group.draw(screen)
    screen.blit(text_surface, text_rect)
    player.update()
    # player.raycasting()
    # enemy_test.update()
    bullet_group.update()

    # debug line of sight

    # debug
    pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
    pygame.draw.rect(screen, "yellow", player.rect, width=2)

    # update elements
    pygame.display.update()
    clock.tick(fps)
