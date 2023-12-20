from typing import Any
import pygame
from settings import *
import math

# init game
pygame.init()

# create the screen
screen = pygame.display.set_mode((width, height))

# clock
clock = pygame.time.Clock()

# font
font = pygame.font.Font("fonts/PublicPixel-z84yD.ttf", 50)
text_surface = font.render("TANKS", False, "Black")
text_rect = text_surface.get_rect(midbottom = (600, 100))

# background
background = pygame.image.load("graphics/background.png").convert_alpha()
background_surface = pygame.transform.scale(background, (1200, 800))

# player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("player/playersprite/tank1.png").convert_alpha(), 270, player_size) # set to 270 otherwise weird bug
        self.image_base = self.image
        self.pos = pygame.math.Vector2(100, 100)
        self.hitbox_rect = self.image_base.get_rect(center = self.pos) # handle collisions
        self.rect = self.hitbox_rect.copy() # draw player on screen
        self.topspeed = player_max_speed
        self.acceleration = player_acceleration
        self.rotation_angle = 0 # starts at 0, increases with left and right
        self.velocity = 0 # moved out of move method due to failure to do as i wanted

    def player_rotate(self):
        self.angle = self.rotation_angle
        self.image = pygame.transform.rotate(self.image_base, -self.angle) # negative angle for correct direction
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)

    def user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.velocity < self.topspeed:
            self.velocity += self.acceleration
        if keys[pygame.K_DOWN] and self.velocity > -self.topspeed:
            self.velocity -= self.acceleration
        if keys[pygame.K_LEFT]: self.rotation_angle -= 1.5
        if keys[pygame.K_RIGHT]: self.rotation_angle += 1.5

        if not any(keys): # implemented friction behavior to stop player from moving when no key is pressed
            if self.velocity > 0:
                self.velocity -= 2 * self.acceleration
            if self.velocity < 0:
                self.velocity += 2 *self.acceleration

    def move(self):
        direction_vector = pygame.math.Vector2(self.velocity, 0).rotate(self.rotation_angle)
        self.pos += direction_vector
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.player_rotate()

player = Player()

# title and icon
pygame.display.set_caption("Tanks")
icon = pygame.image.load("tank1.png")
pygame.display.set_icon(icon)

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # surface placement test
    screen.blit(background_surface, (0, 0))
    screen.blit(player.image, player.rect)
    screen.blit(text_surface, text_rect)
    player.update()

    # debug
    # pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
    # pygame.draw.rect(screen, "yellow", player.rect, width=2)

    # update elements
    pygame.display.update()
    clock.tick(fps)

    # rbg background
    screen.fill((0, 0, 0))