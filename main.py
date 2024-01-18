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

# gun class (somehow need 2 separate classes for player and guns...)
class Gun(pygame.sprite.Sprite):
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
        # self.image_1 = pygame.transform.rotozoom(pygame.image.load(f"player/playersprite/tank_{self.id}_gun.bmp").convert_alpha(), 0, self.gun_size) # gun of the tank
        self.image_base = self.image
        # self.image_base_1 = self.image_1
        self.pos = pygame.math.Vector2(self.x, self.y)
        self.hitbox_rect = self.image_base.get_rect(center = self.pos) # handle collisions
        self.rect = self.hitbox_rect.copy() # draw player on screen
        # self.gun_pos = pygame.math.Vector2(self.x, self.y)
        # self.gun_hitbox_rect = self.image_base_1.get_rect(center = self.gun_pos)
        # self.gun_rect = self.gun_hitbox_rect.copy()
        self.rotation_angle = 0 # starts at 0, increases with left and right
        self.velocity = 0 # moved out of move method due to failure to do as i wanted
        self.shoot_cooldown = 0
        self.shooting = False # bool
        self.strictly_above = False
        self.strictly_below = False
        self.strictly_left = False
        self.strictly_right = False
        self.colliding_o = False
        self.colliding_p = False
        self.angle_index = 0 # used in ray casting algorithm
        self.gun = Gun(self.pos[0], self.pos[1], self.gun_size, self.id) # init gun
        Player.playerInstances.append(self) # appends instance to class list

    def player_rotate(self):
        self.angle = self.rotation_angle
        self.image = pygame.transform.rotate(self.image_base, -self.angle) # negative angle for correct direction
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)

    def gun_rotate(self): # implement code to make sure gun rotates along with the mouse cursor
        if not self.ai: # if controlled by player, mouse controls gun rotation
            self.mouse_coords = pygame.mouse.get_pos()
            self.delta_change_x = (self.mouse_coords[0] - self.hitbox_rect.centerx)
            self.delta_change_y = (self.mouse_coords[1] - self.hitbox_rect.centery)
            self.gun_angle = math.degrees(math.atan2(self.delta_change_y, self.delta_change_x))
            self.gun.image = pygame.transform.rotate(self.gun.image_base, -self.gun_angle)
            self.gun.rect = self.gun.image.get_rect(center = self.gun.hitbox_rect.center)
        else: # implement some form of AI to aim at other tanks!
            for playerinstance in Player.playerInstances: # check all class instances
                if playerinstance.id != self.id: # checks if instance is not self
                    self.aim_coords = playerinstance.pos
                    self.delta_change_x = (self.aim_coords[0] - self.gun.hitbox_rect.centerx)
                    self.delta_change_y = (self.aim_coords[1] - self.gun.hitbox_rect.centerx)
                    self.gun_angle = math.degrees(math.atan2(self.delta_change_y, self.delta_change_x))
                    self.gun.image = pygame.transform.rotate(self.gun.image_base, -self.gun_angle)
                    self.gun.rect = self.gun.image.get_rect(center = self.gun.hitbox_rect.center)
        self.reset_rotation_angle()

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
            if keys[pygame.K_LEFT]:
                self.rotation_angle -= 1.5
            if keys[pygame.K_RIGHT]:
                self.rotation_angle += 1.5

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
            self.bullet = Bullet(self.gun.rect.centerx + self.x_offset, self.gun.rect.centery + self.y_offset, self.gun_angle)
            bullet_group.add(self.bullet)
            self.is_shooting()

    def reset_rotation_angle(self):
        if self.rotation_angle < 0 and abs(self.rotation_angle) == 360: # full rotation achieved
            self.rotation_angle = 0 # simply resets angle to 0 to prevent larger angles
        if self.rotation_angle > 0 and abs(self.rotation_angle) == 360:
            self.rotation_angle = 0

    def move(self):
        if not self.colliding_o:
            self.direction_vector = pygame.math.Vector2(self.velocity, 0).rotate(self.rotation_angle) # handles movement of tank
            self.pos += self.direction_vector
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
            self.gun.gun_pos += self.direction_vector
            self.gun.hitbox_rect.center = self.gun.gun_pos
            self.gun.rect.center = self.gun.hitbox_rect.center

        # random movement for an ai
        if self.ai:
            pass

    def cast_rays(self): # check 2 and 3 corner case (you never see more)
        for instance in Obstacles.obstaclesInstances: # obstacles objects
            self.closest_angles_coords = {}
            self.how_many_visible_angles = {}
            self.intersections = {} # save intersection coords from line_intersect
            self.screen_corner_rays_intersect = {}
            self.strictly_above = False
            self.strictly_below = False
            self.strictly_left = False
            self.strictly_right = False
            tleft = instance.tleft
            tright = instance.tright
            bleft = instance.bleft
            bright = instance.bright
            # calc distance to each corner of obstacle, index is identical to index of coords
            self.abs_pos = [
                math.sqrt((((self.pos[0] - tleft[0])**2) + (self.pos[1] - tleft[1])**2)),
                math.sqrt((((self.pos[0] - tright[0])**2) + (self.pos[1] - tright[1])**2)),
                math.sqrt((((self.pos[0] - bleft[0])**2) + (self.pos[1] - bleft[1])**2)),
                math.sqrt((((self.pos[0] - bright[0])**2) + (self.pos[1] - bright[1])**2))
                ] # abs distance between tanks centers and obstacle corners

            top = tleft[1]
            bottom = bleft[1]
            left = tleft[0]
            right = bright[0]

            # calculate the x and y offset between player and corners (need for trigonometry)
            offset_x_left = (left - self.pos[0])
            offset_x_right = (right - self.pos[0])
            offset_y_top = (top - self.pos[1])
            offset_y_low = (bottom - self.pos[1])

            self.angles_to_corners = {
            0 : math.atan2(offset_y_top, offset_x_left),
            1 : math.atan2(offset_y_top, offset_x_right),
            2 : math.atan2(offset_y_low, offset_x_left),
            3 : math.atan2(offset_y_low, offset_x_right)
            }

            # determine all start and end points of rays the engine is to draw

            # ray_tleft = ((self.pos[0], self.pos[1]), (tleft[0], tleft[1])) # self to tleft
            # ray_tright = ((self.pos[0], self.pos[1]), (tright[0], tright[1])) # self to tright
            # ray_bleft = ((self.pos[0], self.pos[1]), (bleft[0], bleft[1])) # self to tleft
            # ray_bright = ((self.pos[0], self.pos[1]), (bright[0], bright[1])) # self to tright

            # these will be used to compute intersections between rays and other objects
            vertice_top = (tleft, tright) # top side of obstacle rectangle
            vertice_bottom = (bleft, bright) # bottom side of obstacle rectangle
            vertice_left = (tleft, bleft) # left side of obstacle rectangle
            vertice_right = (tright, bright) # right side of obstacle rectangle
            screen_top = ((0, 0), (width, 0))
            screen_bottom = ((0, height), (width, height))
            screen_left = ((0, 0), (0, height))
            screen_right = ((width, 0), (width, height))

            obstacle_vertices = [vertice_top, vertice_right, vertice_bottom, vertice_left]
            screen_segments = [screen_top, screen_bottom, screen_left, screen_right]

            # 2 corners visible case: check if player between right left, top bottom
            # 2 can be true at most, above and right/left etc etc
            # !!! order -> 0, 1, 2, 3 = tleft, tright, bleft, bright
            if self.pos[1] <= top: # above the obstacle
                self.strictly_above = True # strictly as in i see 2 corners not 3
                self.how_many_visible_angles[0] = tleft
                self.how_many_visible_angles[1] = tright
                if self.hitbox_rect.colliderect(instance.hitbox_rect): # handle collisions
                    self.pos.y -= 1
                    self.gun.gun_pos.y -= 1
                # pygame.draw.polygon(screen, "red", [self.pos, tleft, tright])
            if self.pos[1] >= bottom: # below the obstacle
                self.strictly_below = True
                self.how_many_visible_angles[2] = bleft
                self.how_many_visible_angles[3] = bright
                if self.hitbox_rect.colliderect(instance.hitbox_rect): # handle collisions
                    self.pos.y += 1
                    self.gun.gun_pos.y += 1
                # pygame.draw.polygon(screen, "red", [self.pos, bleft, bright])
            if self.pos[0] <= left: # left of the obstacle
                self.strictly_left = True
                self.how_many_visible_angles[0] = tleft
                self.how_many_visible_angles[2] = bleft
                if self.hitbox_rect.colliderect(instance.hitbox_rect): # handle collisions
                    self.pos.x -= 1
                    self.gun.gun_pos.x -= 1
                # pygame.draw.polygon(screen, "red", [self.pos, tleft, bleft])
            if self.pos[0] >= right: # right of the obstacle
                self.strictly_right = True
                self.how_many_visible_angles[1] = tright
                self.how_many_visible_angles[3] = bright
                if self.hitbox_rect.colliderect(instance.hitbox_rect): # handle collisions
                    self.pos.x += 1
                    self.gun.gun_pos.x += 1
                # pygame.draw.polygon(screen, "red", [self.pos, tright, bright])

            # find key (index equivalent) of 3 closest angles
            self.abs_pos_clone = self.abs_pos.copy() # copy the abs_pos list to a new list
            self.cl0 = self.abs_pos.index(min(self.abs_pos_clone)) # closest0..
            self.abs_pos_clone[self.cl0] = 100000 # replace to n to find second closest
            self.cl1 = self.abs_pos.index(min(self.abs_pos_clone))
            self.abs_pos_clone[self.cl1] = 100000 # replace to n to find third closest
            self.cl2 = self.abs_pos.index(min(self.abs_pos_clone))

            # find angles of closest points based on cl index
            self.ag0 = self.angles_to_corners[self.cl0] # angle of closest corner (radians)
            self.ag1 = self.angles_to_corners[self.cl1] # .. 2nd closest ..
            self.ag2 = self.angles_to_corners[self.cl2]

            # intersection between line(p1, p2) and line(p3, p4)
            # https://gist.github.com/kylemcdonald/6132fc1c29fd3767691442ba4bc84018
            def intersect(line1, line2):
                x1, y1 = line1[0][0], line1[0][1]
                x2, y2 = line1[1][0], line1[1][1]
                x3, y3 = line2[0][0], line2[0][1]
                x4, y4 = line2[1][0], line2[1][1]
                denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
                if denom == 0: # parallel
                    return False
                ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
                if ua < 0 or ua > 1: # out of range
                    return False
                ub = ((x2 - x1) * (y1-y3) - (y2 - y1) * (x1 - x3)) / denom
                if ub < 0 or ub > 1: # out of range
                    return False
                x = x1 + ua * (x2 - x1)
                y = y1 + ua * (y2 - y1)
                return (x, y)

            # get endpoints of lines from self to corners of the screen
            self.tleft_corner_line = (tuple(self.pos), (0, 0))
            self.tright_corner_line = ((self.pos[0], self.pos[1]), (width, 0))
            self.bleft_corner_line = ((self.pos[0], self.pos[1]), (0, height))
            self.bright_corner_line = ((self.pos[0], self.pos[1]), (width, height))

            corner_rays = [self.tleft_corner_line, self.tright_corner_line, self.bleft_corner_line, self.bright_corner_line]

            pygame.draw.line(screen, "white", self.pos, (0, 0), 2)
            pygame.draw.line(screen, "white", self.pos, (width, 0), 2)
            pygame.draw.line(screen, "white", self.pos, (0, height), 2)
            pygame.draw.line(screen, "white", self.pos, (width, height), 2)

            # compute intersection (if any) between corners and self rays
            # works fine, but need to absolutely change the data structure i use here -> (not optimal)
            # TO DO -> REWRITE THIS
            self.dist_intersect = []
            self.intersections = []
            for ray in corner_rays:
                for vertice in obstacle_vertices: # 1 ray, check 4 vertices (at most 2 non False)
                    self.intersect_coord = intersect(ray, vertice) # corner rays and vertices
                    self.intersections.append(self.intersect_coord) # appends both x, y or False
                    if self.intersect_coord is not False: # might as well use math.dist ...
                        self.dist_intersect.append((((self.pos[0] - self.intersect_coord[0])**2 + self.pos[1] - self.intersect_coord[1])**2)**0.5)
                    else:
                        self.dist_intersect.append(False)
                # debug intersection coordinates to check if result is correct
                # -> result seems to be correct ?
                self.intersections = [i for i in self.intersections if i is not False]
                self.dist_intersect = [i for i in self.dist_intersect if i is not False]
                if len(self.dist_intersect) > 0:
                    self.min_dist_to_intersect = self.dist_intersect.index(min(self.dist_intersect))
                    self.first_intersect = self.intersections[self.min_dist_to_intersect]
                    pygame.draw.circle(screen, "green", self.first_intersect, 6, 3)

            # draw debugging triangle to visualize line of sight
            self.true_flags = sum([self.strictly_above, self.strictly_below, self.strictly_left, self.strictly_right])
            if self.true_flags == 1: # case where 1 side of an obstacle are visible
                self.corner_x_0 = self.pos[0] + 20*self.abs_pos[self.cl0] * math.cos(self.ag0)
                self.corner_y_0 = self.pos[1] + 20*self.abs_pos[self.cl0] * math.sin(self.ag0)
                self.corner_x_1 = self.pos[0] + 20*self.abs_pos[self.cl1] * math.cos(self.ag1)
                self.corner_y_1 = self.pos[1] + 20*self.abs_pos[self.cl1] * math.sin(self.ag1)
                self.closest_angles_coords[0] = (self.corner_x_0, self.corner_y_0)
                self.closest_angles_coords[1] = (self.corner_x_1, self.corner_y_1)
                # draw the rays to the corners calculated above
                pygame.draw.line(screen, "red", self.pos, self.closest_angles_coords[0], 2)
                pygame.draw.line(screen, "blue", self.pos, self.closest_angles_coords[1], 2)
                # turn rays into line segments [a, b] to check intersections
                self.ray0 = (self.pos, self.closest_angles_coords[0])
                self.ray1 = (self.pos, self.closest_angles_coords[1])
                # compute intersections - rays and obstacles (before screen borders!)

            if self.true_flags == 2: # case where 2 sides of an obstacle are visible
                self.corner_x_0 = self.pos[0] + self.abs_pos[self.cl0] * math.cos(self.ag0)
                self.corner_y_0 = self.pos[1] + self.abs_pos[self.cl0] * math.sin(self.ag0)
                self.corner_x_1 = self.pos[0] + 20*self.abs_pos[self.cl1] * math.cos(self.ag1)
                self.corner_y_1 = self.pos[1] + 20*self.abs_pos[self.cl1] * math.sin(self.ag1)
                self.corner_x_2 = self.pos[0] + 20*self.abs_pos[self.cl2] * math.cos(self.ag2)
                self.corner_y_2 = self.pos[1] + 20*self.abs_pos[self.cl2] * math.sin(self.ag2)
                self.closest_angles_coords[0] = (self.corner_x_0, self.corner_y_0)
                self.closest_angles_coords[1] = (self.corner_x_1, self.corner_y_1)
                self.closest_angles_coords[2] = (self.corner_x_2, self.corner_y_2)
                # draw the rays to the corners calculated above
                pygame.draw.line(screen, "red", self.pos, self.closest_angles_coords[0], 2)
                pygame.draw.line(screen, "red", self.pos, self.closest_angles_coords[1], 2)
                pygame.draw.line(screen, "red", self.pos, self.closest_angles_coords[2], 2)

            # debug
            # print("id", instance.id)
            # print("pos", self.pos)
            # print("angles", self.ag0, self.ag1, self.ag2)
            # print("angle index", self.cl0, self.cl1, self.cl2)
            # print("distance", self.abs_pos)
            # print("angles (radians)", self.angles_to_corners)
            # print("resulting coords", self.closest_angles_coords)
            # print("#################################################")

    def draw_line_of_sight(self):
        pass

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
                    
    def is_killed(self):
        if self.health == 0:
            self.kill()
            self.gun.kill()
            self.pos = (10000, 10000)

    def update(self):
        self.user_input()
        self.move()
        self.player_rotate()
        self.gun_rotate()
        self.is_shooting()
        self.ai_incentive()
        self.is_killed()
        self.raycasting()

    def raycasting(self):
        self.cast_rays()
        self.draw_line_of_sight()

# bullet class
class Bullet(pygame.sprite.Sprite): # should update to differentiate between player and ai
    bulletInstances = []
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
   
    def bullet_collide(self):
        other_bullets = [instance for instance in Bullet.bulletInstances if instance.pos != self.pos] # all bullets except self
        for instance in other_bullets:
            if self.hitbox_rect.colliderect(instance.hitbox_rect): # checks coll with bullets
                self.kill()
                instance.kill()
        for obstacle in Obstacles.obstaclesInstances:
            if self.hitbox_rect.colliderect(obstacle.hitbox_rect):
                self.kill()
        for player_inst in Player.playerInstances:
            if self.hitbox_rect.colliderect(player_inst.hitbox_rect):
                player_inst.health -= player_bullet_dmg
                self.kill()

    def update(self):
        self.move_bullet()
        self.bullet_collide()
        
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

# enemy_test = Player(400, 400, health=100, ai = True, idn = 1) # ai instance

obstacle_test = Obstacles(600, 600, 0, 1) # obstacle test
obstacle_test_2 = Obstacles(800, 200, 1, 1)

player_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

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
