import pygame
import sys
import numpy as np
from helper import *

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

TILE_SIZE = 50
GRID_W, GRID_H = 2000, 2000

WIDTH, HEIGHT = screen.get_size()
NUM_CELLS_H, NUM_CELLS_V = GRID_W // TILE_SIZE, GRID_H // TILE_SIZE

camera_offset = [GRID_W//2, GRID_H//2]

cells = np.random.randint(2, size=(NUM_CELLS_V, NUM_CELLS_H))

# Colors
BACKGROUND = (30,30,30)
CELL_COLOR = (200,200,200)
LINE_COLOR = (128, 128, 128)


while True:
    dt = clock.tick(30) / 1000

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                # Updating game
                cells = apply_rules(cells)

    camera_offset = get_camera_offset(pygame.key.get_pressed(), camera_offset, dt)

    screen.fill(BACKGROUND)

    # Draw cells
    for y in range(NUM_CELLS_V):
        for x in range(NUM_CELLS_H):
            cell_state = cells[y][x]
            if not cell_state:
                continue
            cell_rect = pygame.Rect((x * TILE_SIZE - camera_offset[0], y * TILE_SIZE - camera_offset[1], TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, CELL_COLOR, cell_rect)

    # Draw grid
    line_thickness = 2
    for x in range(0, GRID_W, TILE_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x - camera_offset[0], 0 - camera_offset[1]), (x - camera_offset[0], GRID_H - camera_offset[1]), line_thickness)
    for y in range(0, GRID_H, TILE_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0 - camera_offset[0], y - camera_offset[1]), (GRID_W - camera_offset[0], y - camera_offset[1]), line_thickness)

    pygame.display.flip()
