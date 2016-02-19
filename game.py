from board import *
from player import *

class Log:
    def __init__(self):
        self.series = []
        self.cur = -1

    def add(self, moves):
        if self.cur != len(self.series) - 1:
            self.series = self.series[0:self.cur + 1]

        self.series.append(moves)
        self.cur += 1

    def nextLog(self):
        if self.cur < len(self.series) - 1:
            self.cur += 1
            r = self.series[self.cur]
            return r
        else:
            return []

    def prevLog(self):
        if self.cur > -1:
            r = self.series[self.cur]
            self.cur -= 1
            return r
        else:
            return []

class Game:
    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.log = Log()
        self.turn = 0

    def updateTurn(self):
        self.turn = (self.turn + 1) % 2

    def reset(self):
        for i in range(1, SIZE - 1):
            for j in range(1, SIZE - 1):
                self.board.board[i][j] = Empty
        self.board.winPlayer = "Draw"
        self.log = Log()
        self.turn = 0

    def isFirst(self):
        return self.log.cur == -1

    def firstMove(self):
        player = self.players[self.turn]
        x, y = player.firstMove()
        self.board.putDown(x, y, player.stone)
        self.updateTurn()
        self.log.add([(x, y)])

    def step(self):
        if not self.isOver():
            player = self.players[self.turn]
            (x1, y1), (x2, y2) = player.move(self.board.board)
            self.board.putDown(x1, y1, player.stone)
            self.board.putDown(x2, y2, player.stone)
            self.updateTurn()
            self.log.add([(x1, y1), (x2, y2)])

    def isOver(self):
        return (self.board.isFull() or self.board.isGameOver())

    def rewind(self, logs, stone):
        if len(logs) != 0:
            for (x, y) in logs:
                self.board.putDown(x, y, stone)
            self.updateTurn()

    def prevStep(self):
        self.rewind(self.log.prevLog(), Empty)

    def nextStep(self):
        self.rewind(self.log.nextLog(), self.players[self.turn].stone)

if __name__ == '__main__':
    from board import *
    from player import *

    p1, p2 = RandomPlayer(B), RandomPlayer(W)

    board = Board()

    players = [p1, p2]
    game = Game(board, players)

    game.firstMove()
    print(board)

    while not game.isOver():
        game.step()
        print(board)

    print("%s won" % board.winPlayer)
