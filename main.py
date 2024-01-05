import pygame
from settings import *
import math
from random import shuffle, randint
from other_functions import * # imports all functions defined outside of main
import sys

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
background = pygame.image.load("graphics/background.bmp").convert_alpha()
background_surface = pygame.transform.scale(background, (width, height))

# pick color function
color_list = [] # append choices of colors here
def pick_color(n):
    global color_list
    while len(color_list) != n:
        choice = randint(0, n - 1)
        if choice in color_list:
            continue
        if choice not in color_list:
            color_list.append(choice)

pick_color(4)

# player class (also will incorporate the enemies and their AI at some stage)
class Player(pygame.sprite.Sprite):
    playerInstances = [] # stores all Player object instances
    def __init__(self, x, y, name = str, health = int, kills = 0, ai = bool, idn = int): # class for tanks
        super().__init__()
        self.x = x
        self.y = y
        self.name = name
        self.health = health
        self.kills = kills
        self.ai = ai
        self.id = idn
        if ai: # according to flag set in constructor - see settings.py file
            self.size = e_size
            self.gun_size = e_gun_size
            self.max_speed = e_max_speed
            self.acceleration = e_acceleration
            self.bullet_velocity = e_bullet_velocity
            self.bullet_size = e_bullet_size
            self.shoot_cooldown = e_shoot_cooldown
        else: # player controlled tank
            self.size = player_size
            self.gun_size = player_gun_size
            self.max_speed = player_max_speed
            self.acceleration = player_acceleration
            self.bullet_velocity = player_bullet_velocity
            self.bullet_size = player_bullet_size
            self.shoot_cooldown = player_shoot_cooldown
        self.image = pygame.transform.rotozoom(pygame.image.load(f"player/playersprite/tank_{self.id}_1.bmp").convert_alpha(), 0, self.size) # body of the tank
        self.image_1 = pygame.transform.rotozoom(pygame.image.load(f"player/playersprite/tank_{self.id}_gun.bmp").convert_alpha(), 0, self.gun_size) # gun of the tank
        self.image_base = self.image
        self.image_base_1 = self.image_1
        self.pos = pygame.math.Vector2(self.x, self.y)
        self.hitbox_rect = self.image_base.get_rect(center = self.pos) # handle collisions
        self.rect = self.hitbox_rect.copy() # draw player on screen
        self.gun_pos = pygame.math.Vector2(self.x, self.y)
        self.gun_hitbox_rect = self.image_base_1.get_rect(center = self.gun_pos)
        self.gun_rect = self.gun_hitbox_rect.copy()
        self.rotation_angle = 0 # starts at 0, increases with left and right
        self.velocity = 0 # moved out of move method due to failure to do as i wanted
        self.shoot_cooldown = 0
        self.shooting = False # bool
        self.strictly_above = False
        self.strictly_below = False
        self.strictly_left = False
        self.strictly_right = False
        self.angle_index = 0 # used in ray casting algorithm
        Player.playerInstances.append(self) # appends instance to class list

    def player_rotate(self):
        self.angle = self.rotation_angle
        self.image = pygame.transform.rotate(self.image_base, -self.angle) # negative angle for correct direction
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)

    def gun_rotate(self): # implement code to make sure gun rotates along with the mouse cursor
        if not self.ai: # if controlled by player, mouse controls gun rotation
            self.mouse_coords = pygame.mouse.get_pos()
            self.delta_change_x = (self.mouse_coords[0] - self.gun_hitbox_rect.centerx)
            self.delta_change_y = (self.mouse_coords[1] - self.gun_hitbox_rect.centery)
            self.gun_angle = math.degrees(math.atan2(self.delta_change_y, self.delta_change_x))
            self.image_1 = pygame.transform.rotate(self.image_base_1, -self.gun_angle)
            self.gun_rect = self.image_1.get_rect(center = self.gun_hitbox_rect.center)
        else: # implement some form of AI to aim at the player!
            for playerinstance in Player.playerInstances: # check all class instances
                if playerinstance.id != self.id: # checks if instance is not self
                    self.aim_coords = playerinstance.pos
                    self.delta_change_x = (self.aim_coords[0] - self.gun_hitbox_rect.centerx)
                    self.delta_change_y = (self.aim_coords[1] - self.gun_hitbox_rect.centerx)
                    self.gun_angle = math.degrees(math.atan2(self.delta_change_y, self.delta_change_x))
                    self.image_1 = pygame.transform.rotate(self.image_base_1, -self.gun_angle)
                    self.gun_rect = self.image_1.get_rect(center = self.gun_hitbox_rect.center)

    def is_shooting(self):
        if self.shooting and self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1 # until it hits 0
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_cooldown
            self.shooting = False

    def user_input(self):
        keys = pygame.key.get_pressed()
        if not self.ai: # ai controlled tanks do not access keyboard
            if keys[pygame.K_UP] and self.velocity < self.max_speed:
                self.velocity += self.acceleration
            if keys[pygame.K_DOWN] and self.velocity > -self.max_speed:
                self.velocity -= self.acceleration
            if keys[pygame.K_LEFT]: self.rotation_angle -= 1.5
            if keys[pygame.K_RIGHT]: self.rotation_angle += 1.5

        if not self.ai and not any(keys): # implemented friction behavior to stop player from moving when no key is pressed
            if self.velocity > 0:
                self.velocity -= 2 * self.acceleration
            if self.velocity < 0:
                self.velocity += 2 *self.acceleration

        if not self.ai and pygame.mouse.get_pressed()[0] and not self.shooting: # left click, check if cooldown expired
            self.shooting = True # set shooting state to True, used in is_shooting method
            self.shoot_cooldown = player_shoot_cooldown # set to whatever, see settings
            self.gun_angle_rad = math.radians(self.gun_angle)
            self.x_offset = (40 * math.cos(self.gun_angle_rad)) # ~ gun length (40)
            self.y_offset = (40 * math.sin(self.gun_angle_rad))
            self.bullet = Bullet(self.gun_rect.centerx + self.x_offset, self.gun_rect.centery + self.y_offset, self.gun_angle)
            bullet_group.add(self.bullet)
            self.is_shooting()
            

    # DOES NOT WORK, NEED TO FIX
    def is_colliding(self):
        for instance in Player.playerInstances:
            relative_dist = [math.sqrt((((self.pos[0] - instance.pos[0])**2) + (self.pos[1] - instance.pos[1])**2)) for instance in Player.playerInstances] # distance between tanks
            for i in relative_dist: # start with 80, see how it behaves later 
                if i == 0:
                    i = 10000 # replaces 0
                if i < 60:
                    self.velocity = 0

    def move(self):
        direction_vector = pygame.math.Vector2(self.velocity, 0).rotate(self.rotation_angle) # handles movement of tank
        self.pos += direction_vector
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
        self.gun_pos += direction_vector
        self.gun_hitbox_rect.center = self.gun_pos
        self.gun_rect.center = self.gun_hitbox_rect.center
        
    def cast_rays(self): # check 2 and 3 corner case (you never see more)
        self.visible_angles = [] # append the corner coordinates in the order i need them in
        self.how_many_visible_angles = []
        self.strictly_above = False
        self.strictly_below = False
        self.strictly_left = False
        self.strictly_right = False
        self.two_angles = False
        self.three_angles = False
        for instance in Obstacles.obstaclesInstances: # list of 4 coords
            tleft = instance.tleft
            tright = instance.tright
            bleft = instance.bleft
            bright = instance.bright
            # calc distance to each corner of obstacle, index is identical to index of coords
            self.abs_pos = [
                math.sqrt((((self.pos[0] - tleft[0])**2) + (self.pos[1] - tleft[1])**2)), 
                math.sqrt((((self.pos[0] - bleft[0])**2) + (self.pos[1] - bright[1])**2)),
                math.sqrt((((self.pos[0] - tright[0])**2) + (self.pos[1] - tright[1])**2)),
                math.sqrt((((self.pos[0] - bright[0])**2) + (self.pos[1] - bright[1])**2))
                ] # abs distance between tanks centers and obstacle corners

            top = tleft[1]
            bottom = bleft[1]
            left = tleft[0]
            right = bright[0]

            # calculate the x and y offset between player and corners (need for trigonometry)
            offset_x_left = abs(self.pos[0] - left)
            offset_x_right = abs(self.pos[0] - right)
            offset_y_top = abs(self.pos[1] - top)
            offset_y_low = abs(self.pos[1] - bottom)

            # calculate the angles between player pos and all corners (radians for later use)
            self.angles_to_corners = [
            math.atan(offset_y_top / offset_x_left),
            math.atan(offset_y_top/ offset_x_right),
            math.atan(offset_y_low / offset_x_left),
            math.atan(offset_y_low / offset_x_right)
            ]

            self.angles_to_corners_degrees = [math.degrees(angle) for angle in self.angles_to_corners]

            # 2 corners visible case: check if player between right left, top bottom
            # 2 can be true at most, above and right/left etc etc
            if self.pos[1] < top: # between left and right, and above the obstacle
                self.strictly_above = True # strictly as in i see 2 corners not 3
                self.how_many_visible_angles.append(tleft)
                self.how_many_visible_angles.append(tright)
                pygame.draw.polygon(screen, "red", [self.pos, tleft, tright])
                print("on top")
            if self.pos[1] > bottom: # between left and right, and below the obstacle
                self.strictly_below = True
                self.how_many_visible_angles.append(bleft)
                self.how_many_visible_angles.append(bright)
                pygame.draw.polygon(screen, "red", [self.pos, bleft, bright])
                print("below")
            if self.pos[0] < left: # between top and bottom, and left of the obstacle
                self.strictly_left = True
                self.how_many_visible_angles.append(tleft)
                self.how_many_visible_angles.append(bleft)
                pygame.draw.polygon(screen, "red", [self.pos, tleft, bleft])
                print("left")
            if self.pos[0] > right: # between top and bottom, and right of the obstacle
                self.strictly_right = True
                self.how_many_visible_angles.append(tright)
                self.how_many_visible_angles.append(bright)
                pygame.draw.polygon(screen, "red", [self.pos, tright, bright])
                print("right")
                
        self.how_many_visible_angles = set(self.how_many_visible_angles)

            # find coordinates of corner points based on the distance and angle from self
            # --> yes we already know the coordinates but this will allow the ray casting
            # algorithm to not make any mistakes and be as precise at it must be
            # if len(self.how_many_visible_angles) == 2:
            #     self.two_angles = True
            #     self.angle_index = 2 # 2 angles are visible
            #     print("2 angles are visible")
            # if len(self.how_many_visible_angles) == 3:
            #     self.three_angles = True
            #     self.angle_index = 3 # 3 angles are visible
            #     print("3 angles are visible")
            # for i, distance in enumerate(sorted(self.abs_pos[:self.angle_index])):
            #     angle_rad = self.angles_to_corners[i] # problematic code
            #     corner_x = self.pos[0] + distance * math.cos(angle_rad)
            #     corner_y = self.pos[1] + distance * math.sin(angle_rad)
            #     self.visible_angles.append((corner_x, corner_y))
            # # TO DO: FIX THE CODE ABOVE. problem: angle_rad not always correct angle!
            # print(self.how_many_visible_angles)
            # print(self.visible_angles)
            # print(self.angles_to_corners_degrees)


    def draw_line_of_sight(self):
        self.visible_angles = sorted(self.visible_angles)
        if self.two_angles:
            pygame.draw.polygon(screen, "red", [self.pos, self.visible_angles[0], self.visible_angles[1]])
        if self.three_angles:
            pygame.draw.polygon(screen, "red", [self.pos, self.visible_angles[0], self.visible_angles[2]])
            pygame.draw.polygon(screen, "red", [self.pos, self.visible_angles[0], self.visible_angles[1]])
        
        




            

    def ai_incentive(self): # attributes a "score" to determine the best move for ai tanks
        self.best_move_eval = {}
        for instance in Player.playerInstances:
            self.best_move_eval[instance.id] = 0 # 0 score for any n number_of_tanks
        self.best_move = 0 # score always starts at 0, updated with each condition checked
        if self.ai: # if ai, will determine which tank to aim at
            # find closest tank
            for instance in Player.playerInstances: # i allow for self.pos - self.pos
                relative_pos = [math.sqrt((((self.pos[0] - instance.pos[0])**2) + (self.pos[1] - instance.pos[1])**2)) for instance in Player.playerInstances] # abs distance between tanks centers
                relative_pos[relative_pos.index(min(relative_pos))] = 10000 # replaces 0 by large value
                closest_instance_idx = relative_pos.index(min(relative_pos)) # now finds correct index
                # find enemy with lowest health points
                instance_health = [instance.health for instance in Player.playerInstances] # lists health of all tanks
                instance_health[self.id] = 10000 # set arbitrarily large value to own health # NEED TO DEBUG THIS
                lowest_instance_health_idx = instance_health.index(min(instance_health))
                
                # find tank which killed many other tanks (dangerous tank is the logic)
                instance_kills = [instance.kills for instance in Player.playerInstances] # lists kills per instance
                if max(instance_kills) > 0: # checks if any instance has a kill
                    instance_kills[instance_kills.index(min(instance_kills))] = 0 # replace lowest kill count to 0, prevents from targeting self
                    max_instance_kills_idx = instance_kills.index(max(instance_kills)) # find id of tank with highest kill count
                
                # find if a specific tank holds any powerups (can set a danger score for each)
                # needs to be worked on

    def update(self):
        self.user_input()
        self.move()
        self.player_rotate()
        self.gun_rotate()
        self.is_shooting()
        self.is_colliding()
        self.ai_incentive()
        
    def raycasting(self):
        self.cast_rays()
        self.draw_line_of_sight()

# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("player/bulletsprite/bullet_1.bmp").convert_alpha(), 0, player_bullet_size)
        self.image_base = self.image
        self.x = x
        self.y = y
        self.pos = pygame.math.Vector2(x, y)
        self.hitbox_rect = self.image_base.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.velocity = player_bullet_velocity
        self.angle = math.radians(angle)

    def move_bullet(self):
        self.vel_x = self.velocity * math.cos(self.angle)
        self.vel_y = self.velocity * math.sin(self.angle)
        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.pos

    def update(self):
        self.move_bullet()
        
# obstacles class
class Obstacles():
    obstaclesInstances = []
    obstaclesInstancesCorners = [] # save 4 corners of any obstacle (all rectangles)
    obstaclesInstancesSides = [] # appends x, y coords of sides of obstacles
    def __init__(self, x, y, identifier, obstacletype, corners = [], vertices = []):
        super().__init__()
        self.x = x
        self.y = y
        self.id = identifier
        self.type = obstacletype
        self.pos = pygame.math.Vector2(x, y)
        self.image = pygame.transform.rotozoom(pygame.image.load("graphics/obstacles/obstacle.bmp").convert_alpha(), 0, 4)
        self.hitbox_rect = self.image.get_rect(center = self.pos)
        self.tleft = self.hitbox_rect.topleft # gives xy coord of top left corner
        self.tright = self.hitbox_rect.topright
        self.bleft = self.hitbox_rect.bottomleft
        self.bright = self.hitbox_rect.bottomright
        self.top = self.hitbox_rect.top # gives y coord of top vertice
        self.bottom = self.hitbox_rect.bottom
        self.left = self.hitbox_rect.left
        self.right = self.hitbox_rect.right
        self.corners = corners # list of 4 corner coordinates
        self.vertices = vertices # list of 4 x and y coordinates for sides of each obstacle

        Obstacles.obstaclesInstances.append(self)

        self.corners.append(self.tleft)
        self.corners.append(self.tright)
        self.corners.append(self.bleft)
        self.corners.append(self.bright)
        self.vertices.append(self.top)
        self.vertices.append(self.bottom)
        self.vertices.append(self.left)
        self.vertices.append(self.right)

# power up class (to do: speed, dmg, health ...)
class powerUps(pygame.sprite.Sprite):
    def __init__(self, x, y, identifier, name, health, points):
        super().__init__()
        self.x = x
        self.y = y
        self.id = identifier
        self.name = name
        self.health = health
        self.points = points

    def spawn(self):
        pass
        # TO DO : set a random spawn point, or not according to map, and work the collisions out.. (should be as simple as playerinstance.rect - powerupinstance = 0 collide ?)

player = Player(100, 100, health=100, ai = False, idn = 0) # player

enemy_test = Player(400, 400, health=100, ai = True, idn = 1) # ai instance

obstacle_test = Obstacles(600, 600, 0, 1) # obstacle test
obstacle_test_2 = Obstacles(800, 200, 0, 1)

player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# add player to group
player_group.add(player) # only adds the main body of the player? fix? else blit
player_group.add(enemy_test)

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
    #enemy gun blit
    screen.blit(enemy_test.image_1, enemy_test.gun_rect)
    #####
    screen.blit(player.image_1, player.gun_rect)
    bullet_group.draw(screen)
    screen.blit(text_surface, text_rect)
    screen.blit(obstacle_test.image, obstacle_test.hitbox_rect)
    screen.blit(obstacle_test_2.image, obstacle_test_2.hitbox_rect)
    player.update()
    player.raycasting()
    enemy_test.update()
    bullet_group.update()

    # debug
    pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
    pygame.draw.rect(screen, "yellow", player.rect, width=2)
    pygame.draw.rect(screen, "red", enemy_test.hitbox_rect, width=2)
    pygame.draw.rect(screen, "yellow", enemy_test.rect, width=2)

    # update elements
    pygame.display.update()
    clock.tick(fps)
