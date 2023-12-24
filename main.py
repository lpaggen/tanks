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
background_surface = pygame.transform.scale(background, (width, height))

# player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("player/playersprite/tank_1.bmp").convert_alpha(), 0, player_size) # body of the tank
        self.image_1 = pygame.transform.rotozoom(pygame.image.load("player/playersprite/tank_gun.bmp").convert_alpha(), 0, gun_size) # gun of the tank
        self.image_base = self.image
        self.image_base_1 = self.image_1
        self.pos = pygame.math.Vector2(100, 100)
        self.hitbox_rect = self.image_base.get_rect(center = self.pos) # handle collisions
        self.rect = self.hitbox_rect.copy() # draw player on screen
        self.gun_pos = pygame.math.Vector2(100, 100)
        self.gun_hitbox_rect = self.image_base_1.get_rect(center = self.gun_pos)
        self.gun_rect = self.gun_hitbox_rect.copy()
        self.topspeed = player_max_speed
        self.acceleration = player_acceleration
        self.rotation_angle = 0 # starts at 0, increases with left and right
        self.velocity = 0 # moved out of move method due to failure to do as i wanted
        self.shoot_cooldown = 0
        self.shooting = False # bool

    def player_rotate(self):
        self.angle = self.rotation_angle
        self.image = pygame.transform.rotate(self.image_base, -self.angle) # negative angle for correct direction
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)

    def gun_rotate(self): # implement code to make sure gun rotates along with the mouse cursor
        self.mouse_coords = pygame.mouse.get_pos()
        self.delta_change_x = (self.mouse_coords[0] - self.gun_hitbox_rect.centerx)
        self.delta_change_y = (self.mouse_coords[1] - self.gun_hitbox_rect.centery)
        self.gun_angle = math.degrees(math.atan2(self.delta_change_y, self.delta_change_x))
        self.image_1 = pygame.transform.rotate(self.image_base_1, -self.gun_angle)
        self.gun_rect = self.image_1.get_rect(center = self.gun_hitbox_rect.center)

    def is_shooting(self):
        if self.shooting:
            self.shoot_cooldown == shoot_cooldown
            self.shoot_cooldown -= 1 # refreshes 60 times per second
            self.bullet = Bullet(self.gun_rect.centerx, self.gun_rect.centery)
            self.bullet.move_bullet()
            if self.shoot_cooldown == 0:
                self.shooting = False

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

        if pygame.mouse.get_pressed()[0] and self.shoot_cooldown == 0: # left click, check if cooldown expired
            self.shooting = True # set shooting state to True, used in is_shooting method

    def move(self):
        direction_vector = pygame.math.Vector2(self.velocity, 0).rotate(self.rotation_angle) # handles movement of tank
        self.pos += direction_vector
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
        self.gun_pos += direction_vector
        self.gun_hitbox_rect.center = self.gun_pos
        self.gun_rect.center = self.gun_hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.player_rotate()
        self.gun_rotate()
        self.is_shooting()

# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("player/bulletsprite/bullet_1.bmp"), 0, bullet_size)
        self.image_base = self.image
        self.x = x
        self.y = y
        self.pos = pygame.math.Vector2(x, y)
        self.hitbox_rect = self.image_base.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.velocity = bullet_velocity
        self.angle = math.radians(player.angle)

    def move_bullet(self):
        self.vel_x = self.velocity * math.cos(self.angle)
        self.vel_y = self.velocity * math.sin(self.angle)
        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)

    def bullet_update(self):
        self.move_bullet()

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
    screen.blit(player.image_1, player.gun_rect) # coordinates for gun of tank to spawn
    screen.blit(text_surface, text_rect)
    player.update()

    # debug
    pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
    pygame.draw.rect(screen, "yellow", player.rect, width=2)

    # update elements
    pygame.display.update()
    clock.tick(fps)

    # rbg background
    screen.fill((0, 0, 0))