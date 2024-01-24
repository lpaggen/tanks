import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class MapEditor:
    def __init__(self):
        self.obstacles = pygame.sprite.Group()
        self.selected_obstacle = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click
                    x, y = 111, 111# just need to find a way to get the coords and the center in order to spawn the obstacle
                    pass
