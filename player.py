from board import SIZE, B, W, Empty, Edge
import random

class Player:
    def __init__(self, stone):
        self.stone = stone
        self.opponent = - stone

    def firstMove(self):
        return (10, 10)

    # return [(x1, y1), (x1, y1)]
    def move(self, board):
        raise NotImplementedError

class RandomPlayer(Player):
    def collectEmpty(self, board):
        return [(i, j) for j in range (SIZE) for i in range(SIZE) if board[i][j] == Empty]

    def move(self, board):
        empty = self.collectEmpty(board)
        candidates = random.sample(empty, 2)
        return candidates
