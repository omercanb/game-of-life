import pygame
import sys
import numpy as np
from helper import apply_rules, get_camera_offset

class GameOfLifeBoard():
    def __init__(self, size, cells = None):
        self.size = size
        self.cells = cells


        if type(self.cells) != np.ndarray:
            self.initialize_cells()

    def initialize_cells(self):
        self.cells = np.random.randint(2, size=(self.size))

    def step(self):
        self.cells = apply_rules(self.cells)



class BoardDrawer():
    TILE_SIZE = 50
    LINE_THICKNESS = 2

    # Colors
    BACKGROUND = (30,30,30)
    CELL_COLOR = (200,200,200)
    LINE_COLOR = (128, 128, 128)

    START_STOP_KEY = pygame.K_s

    def __init__(self, board: GameOfLifeBoard):
        pygame.init()
        self.board = board
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.camera_offset = [board.cells.shape[0] * BoardDrawer.TILE_SIZE // 2, board.cells.shape[1] * BoardDrawer.TILE_SIZE // 2]
        self.number_of_vertical_cells = board.cells.shape[0]
        self.number_of_horizontal_cells = board.cells.shape[1]
        pygame.display.set_caption("Conway's Game of Life")
        self.autoplaying = False

    def draw(self):
        self.dt = self.clock.tick(60) / 1000
        self.screen.fill(BoardDrawer.BACKGROUND)
        # Draw cells
        for y in range(self.number_of_vertical_cells):
            for x in range(self.number_of_horizontal_cells):
                cell_state = self.board.cells[y][x]
                if not cell_state:
                    continue
                cell_rect = pygame.Rect((x * BoardDrawer.TILE_SIZE - self.camera_offset[0], y * BoardDrawer.TILE_SIZE - self.camera_offset[1], 
                                         BoardDrawer.TILE_SIZE, BoardDrawer.TILE_SIZE))
                pygame.draw.rect(self.screen, BoardDrawer.CELL_COLOR, cell_rect)

        # Draw grid
        for x in range(0, self.number_of_horizontal_cells * BoardDrawer.TILE_SIZE, BoardDrawer.TILE_SIZE):
            pygame.draw.line(self.screen, BoardDrawer.LINE_COLOR, (x - self.camera_offset[0], 0 - self.camera_offset[1]), 
                             (x - self.camera_offset[0], self.number_of_vertical_cells * BoardDrawer.TILE_SIZE - self.camera_offset[1]), BoardDrawer.LINE_THICKNESS)
        for y in range(0, self.number_of_vertical_cells * BoardDrawer.TILE_SIZE, BoardDrawer.TILE_SIZE):
            pygame.draw.line(self.screen, BoardDrawer.LINE_COLOR, (0 - self.camera_offset[0], y - self.camera_offset[1]), 
                             (self.number_of_horizontal_cells * BoardDrawer.TILE_SIZE - self.camera_offset[0], y - self.camera_offset[1]), BoardDrawer.LINE_THICKNESS)

        pygame.display.flip()

    def events(self):
    # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE and self.autoplaying == False:
                    # Updating game
                    self.board.step()
                if event.key == BoardDrawer.START_STOP_KEY:
                    if self.autoplaying == False:
                        self.autoplay()
                    else:
                        self.autoplaying = False

        self.camera_offset = get_camera_offset(pygame.key.get_pressed(), self.camera_offset, self.dt)

    def autoplay(self):
        self.autoplaying = True
        timer = 0
        while True:
            self.draw()
            self.events()
            timer += self.dt
            if timer > 0.2:
                self.board.step()
                timer = 0
            if self.autoplaying == False:
                break

    
