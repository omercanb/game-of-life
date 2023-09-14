import numpy as np
from board import GameOfLifeBoard

class Grower():
    #Given a range of cells to build in do a random amount of trials and give the best result in terms of distance
    def __init__(self, size, num_organisms, steps, board_size):
        self.size = size
        self.num_organisms = num_organisms
        self.steps = steps
        self.organisms = []
        self.board_size = board_size
        self.members = []
        self.create_organisms(num_organisms)

    def create_organisms(self, num_organisms):
        for i in range(num_organisms):
            pad_top = self.board_size[0]//2 - self.size[0]//2
            pad_bottom = self.board_size[0] - self.size[0] - pad_top
            pad_right = self.board_size[1] - self.size[1]

            organism = np.random.randint(2, size=(self.size))
            start_cells = np.pad(organism, ((pad_top, pad_bottom), (0, pad_right)), 'constant')
            # cells = np.zeros(self.board_size)
            # cell_insert_pos = cells.shape[0]//2 - self.size[0]
            board = GameOfLifeBoard(self.board_size, start_cells)
            self.members.append({'value':0,'org':organism,'start':start_cells,'board':board})

    def value(self, board):
        return self.value_sum(board)
    
    def value_distance(self, board):
        return np.max(board.cells.argmax(axis=1))
    
    def value_sum(self, board):
        return board.cells.sum()

    
    def race(self):
        for step in range(self.steps):
            if step % 10 == 0:
                print("Step: "+ str(step))
            for member in self.members:
                old_value = member['value']
                member['board'].step()
                member['value'] = max(old_value, self.value(member['board']))
        self.members.sort(key = lambda member: member['value'], reverse=True)
        print("Step: "+ str(step))

    def topK(self, k):
        return self.members[:k]



        

    
    

    