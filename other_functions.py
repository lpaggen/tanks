from random import randint, shuffle, randrange

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

# determine the intersection of two lines (solve with matrices, see https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines)
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

# calculate distance between two points
def dist(point1, point2):
    return ((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)**0.5

# functions to find second smallest / largest number of list


# function to evenly distribute range into coordinates
def even_space(number = None, number2 = None, bins = None, axis = int):
    if axis not in (0, 1):
        raise ValueError("Axis must be either 0 (x) or 1 (y)")
    step = number / bins # get number of coords to create
    if axis == 0:
        return ([(i * step, 0) for i in range(bins + 1 )], [(i * step, number2) for i in range(bins + 1)])
    if axis == 1:
        return ([(0, i * step) for i in range(bins + 1)], [(number2, i * step) for i in range(bins+ 1 )])

    
