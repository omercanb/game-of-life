import pygame
import sys
import numpy as np
from helper import apply_rules, get_camera_offset
import time
from board import GameOfLifeBoard, BoardDrawer
from grower import Grower


grower = Grower((4,4), 2000, 100, (40,40))
grower.race()
member = grower.topK(1)[0]
board = GameOfLifeBoard((40,40), member['start'])

drawer = BoardDrawer(board)


while True:
    drawer.draw()
    drawer.events()

    