import pygame

# obstacles class
class Obstacle(pygame.sprite.Sprite):
    obstaclesInstances = []
    obstaclesInstancesCorners = [] # save 4 corners of any obstacle (all rectangles) -> UNUSED ATM
    obstaclesInstancesVertices = [] # appends x, y coords of sides of obstacles
    obstacle_group = pygame.sprite.Group()
    def __init__(self, x, y, identifier, obstacletype):
        super().__init__()
        self.x = x
        self.y = y
        self.id = identifier
        self.type = obstacletype
        self.pos = pygame.math.Vector2(x, y)
        self.image = pygame.transform.rotozoom(pygame.image.load("graphics/obstacles/obstacle.bmp").convert_alpha(), 0, 1.875)
        self.hitbox_rect = self.image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.tleft = self.hitbox_rect.topleft # gives xy coord of top left corner
        self.tright = self.hitbox_rect.topright
        self.bleft = self.hitbox_rect.bottomleft
        self.bright = self.hitbox_rect.bottomright
        self.top = self.hitbox_rect.top # gives y coord of top vertice
        self.bottom = self.hitbox_rect.bottom
        self.left = self.hitbox_rect.left
        self.right = self.hitbox_rect.right
        self.v_top = (self.tleft, self.tright) # vertice top, etc (line segments)
        self.v_right = (self.tright, self.bright)
        self.v_bottom = (self.bleft, self.bright)
        self.v_left = (self.bleft, self.tleft)

        Obstacle.obstaclesInstances.append(self)
        Obstacle.obstacle_group.add(self)

        Obstacle.obstaclesInstancesVertices.append(self.v_top) # vertice top
        Obstacle.obstaclesInstancesVertices.append(self.v_right) # right ..
        Obstacle.obstaclesInstancesVertices.append(self.v_bottom)
        Obstacle.obstaclesInstancesVertices.append(self.v_left)
