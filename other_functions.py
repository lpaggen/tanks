from random import randint, shuffle, randrange
from settings import *
import main

# pick color function
color_list = [] # list of n different integers, serves to find different bmp for colors
def pick_color(n):
    global color_list
    while len(color_list) != n:
        choice = randint(0, n - 1)
        if choice in color_list:
            continue
        if choice not in color_list:
            color_list.append(choice)

# create all n tank objects (currently max supported 4, can make modular by increasing coords)
def init_tanks(number_of_tanks):
    pick_color(number_of_tanks)
    tankid = color_list[0] # used for colors, and spawn positions
    color_list.pop(tankid)
    player = Player(coord_list[tankid][0], coord_list[tankid][1], ai = False, id = tankid)
    for i in range(1, number_of_tanks): # ai controlled tanks are instantiated
        tankid = color_list[i]
        color_list.pop(tankid)
        enemy = Player(coord_list[tankid][0], coord_list[tankid][1], ai = True, id = tankid)

# determine the intersection of two lines (solve with matrices, see https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines)
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# other_players = [instance for instance in Player.playerInstances if instance.id != self.id]
#         for instance in other_players:
#             dx = instance.pos[0] - self.pos[0] # change in x
#             dy = instance.pos[1] - self.pos[1] # change in y
#             scalar = recoil_scalar
#             if self.hitbox_rect.colliderect(instance.hitbox_rect):
#                 self.pos[0] -= dx * scalar # handles body position
#                 self.pos[1] -= dy * scalar
#                 instance.pos[0] += dx * scalar
#                 instance.pos[1] += dx * scalar
#                 self.gun.gun_pos = self.pos # update gun position to match body position
#                 instance.gun.gun_pos = instance.pos
#         for instance in Obstacles.obstaclesInstances: # only allows movement if not facing object
#             off_x = instance.pos[0] - self.pos[0]
#             off_y = instance.pos[1] - self.pos[1] 
#             angle_to_obstacle_center = math.degrees(math.atan2(off_y, off_x))
#             scalar = recoil_scalar
#             if self.hitbox_rect.colliderect(instance.hitbox_rect) and self.rotation_angle < angle_to_obstacle_center + 90 and self.rotation_angle > self.rotation_angle - 90:
#                 self.velocity = 0
#                 self.gun.gun_pos = self.pos
#             else:
#                 self.pos += self.direction_vector
