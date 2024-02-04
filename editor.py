# most of the code is from chatGPT, the point of this project isn't to learn gamedev, i did not bother to do this, i just need a map for my game

import pygame
import sys
from settings import width, height
from obstacle import *
import json

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 60
GRID_COLOR = (0, 255, 0)
OUTLINE_COLOR = (255, 0, 0)
FILL_COLOR = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Advanced Map Editor')

# Boolean grid to represent the state of each cell
grid_width = width // TILE_SIZE
grid_height = height // TILE_SIZE
drawing_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col_index = mouse_x // TILE_SIZE
            row_index = mouse_y // TILE_SIZE

            if event.button == 1:  # Left mouse button
                if drawing_grid[row_index][col_index] == 0:
                    drawing_grid[row_index][col_index] = 1
                else:
                    drawing_grid[row_index][col_index] = 2

            elif event.button == 3:  # Right mouse button
                drawing_grid[row_index][col_index] = 0

    # draw screen
    background = pygame.image.load("graphics/background.bmp").convert_alpha()
    background_surface = pygame.transform.scale(background, (width, height))
    screen.blit(background_surface, (0, 0))

    # Draw the grid
    for row_index in range(grid_height):
        for col_index in range(grid_width):
            pygame.draw.rect(screen, GRID_COLOR, (col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    for row_index, row in enumerate(drawing_grid):
        for col_index, cell in enumerate(row):
            tile_center_x = col_index * TILE_SIZE + TILE_SIZE / 2
            tile_center_y = row_index * TILE_SIZE + TILE_SIZE / 2

            rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if cell == 1:
                # Draw outline
                pygame.draw.rect(screen, OUTLINE_COLOR, rect, 2)
            elif cell == 2:
                # Check if an obstacle already exists at this position
                i = 0
                center_pos = (tile_center_x, tile_center_y)
                if not any(obstacle.rect.collidepoint(center_pos) for obstacle in Obstacle.obstacle_group):
                    obs = Obstacle(tile_center_x, tile_center_y, i, 0)
                    Obstacle.obstacle_group.add(obs)
                    Obstacle.obstacle_group.draw(screen)
                    i += 1
                    # save coords into json file, this way i can also just fetch them in my main game loop
                    with open("map_data.json", "w") as file:
                        obs_coords = []
                        for obs in Obstacle.obstaclesInstances:
                            obs_coord_dct = {"x" : obs.x, "y" : obs.y}
                            obs_coords.append(obs_coord_dct)
                        json.dump(obs_coords, file)

    # draw all obstacle tiles
    Obstacle.obstacle_group.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
