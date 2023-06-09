import pygame
import math
import numpy as np

def apply_rules(cells):
    # Create a padded version of the cells matrix
    padded_cells = np.pad(cells, pad_width=1, mode='constant')

    # Calculate the sum of neighboring cells using array slicing and shifting
    neighbor_sum = (
        padded_cells[:-2, :-2] + padded_cells[:-2, 1:-1] + padded_cells[:-2, 2:] +
        padded_cells[1:-1, :-2] + padded_cells[1:-1, 2:] +
        padded_cells[2:, :-2] + padded_cells[2:, 1:-1] + padded_cells[2:, 2:]
    )

    # Create masks for cell survival and birth
    survival_mask = np.logical_and(cells, np.logical_or(neighbor_sum == 2, neighbor_sum == 3))
    birth_mask = np.logical_and(~cells, neighbor_sum == 3)

    # Update the cells based on the masks
    cells = np.zeros_like(cells)
    cells[survival_mask | birth_mask] = 1

    return cells

PAN_SPEED = 1000

def get_camera_offset(keys, camera_offset, dt):
    delta_camera_offset = [0,0]

    if keys[pygame.K_LEFT]:
        delta_camera_offset[0] -= 1
    if keys[pygame.K_RIGHT]:
        delta_camera_offset[0] += 1
    if keys[pygame.K_UP]:
        delta_camera_offset[1] -= 1
    if keys[pygame.K_DOWN]:
        delta_camera_offset[1] += 1

    length = math.sqrt(delta_camera_offset[0]**2 + delta_camera_offset[1]**2)/PAN_SPEED
    if length == 0:
        return camera_offset
    
    delta_camera_offset = [delta_camera_offset[0]/length, delta_camera_offset[1]/length]
    
    if delta_camera_offset:
        camera_offset[0] += delta_camera_offset[0]*dt
        camera_offset[1] += delta_camera_offset[1]*dt
    
    return camera_offset
        
    