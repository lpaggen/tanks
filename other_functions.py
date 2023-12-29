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
    pick_color(4)
    tankid = color_list[0] # used for colors, and spawn positions
    color_list.pop(tankid)
    player = Player(coord_list[tankid][0], coord_list[tankid][1], ai = False, id = tankid)
    for i in range(1, number_of_tanks): # ai controlled tanks are instantiated
        tankid = color_list[i]
        color_list.pop(tankid)
        enemy = Player(coord_list[tankid][0], coord_list[tankid][1], ai = True, id = tankid)