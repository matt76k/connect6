from board import SIZE, B, W, Empty, Edge
import random

class Player:
    def __init__(self, stone):
        self.stone = stone
        self.opponent = - stone

    def firstMove(self):
        """
            this method is invoked on the first turn.
            first player can puts only one stone on board.
            this method should return 2-tuple, default is (10, 10)
        """
        return (10, 10)

    def move(self, board):
        """
            the structure of board is a 2d list (21x21)
            the surroundings of board is always filled with Edge.
            you can put (x, y)
                where
                    - the range of x and y is 1 to 19.
                    - x represents vertical axis
                    - y represents horizontal axis
            this method should return list which contains two 2-tuple
            (e.g [(6, 17), (12, 15)]).
        """
        raise NotImplementedError

class RandomPlayer(Player):
    def collectEmpty(self, board):
        return [(i, j) for j in range (SIZE) for i in range(SIZE) if board[i][j] == Empty]

    def move(self, board):
        empty = self.collectEmpty(board)
        candidates = random.sample(empty, 2)
        return candidates
