import curses
from board import *
from player import *
from game import *

class CBoard:

    def __init__(self, scr, board):
        self.scr = scr
        self.board = board
        self.X, self.Y = SIZE - 2, SIZE - 2

        self.scr.clear()
        border_line = '+'+(self.X*'-')+'+'
        self.scr.addstr(0, 0, border_line)
        self.scr.addstr(self.Y + 1, 0, border_line)
        for y in range(0, self.Y):
            self.scr.addstr(1 + y, 0, '|')
            self.scr.addstr(1 + y, self.X + 1, '|')
        self.scr.refresh()

    def display(self):
        for i in range(1, self.X + 1):
            for j in range(1, self.Y + 1):
                if self.board.board[i][j] == B:
                    self.scr.addstr(i, j, 'o')
                elif self.board.board[i][j] == W:
                    self.scr.addstr(i, j, 'x')
                else:
                    self.scr.addstr(i, j, ' ')
        self.scr.refresh()

def displayInfo(scr, s):
    scr.move(SIZE, 0)
    scr.clrtoeol()
    scr.addstr(SIZE, 0, s)
    scr.refresh()

def displayMenu(scr):
    scr.addstr(SIZE + 2, 0, "Q) Quit, R) Reset, S) Step 1, E) to the End, P) Prev, N) Next")

def loop(stdscr):

    # set Player here
    # p1 is the first player, p2 is the second player

    p1, p2 = RandomPlayer(B), RandomPlayer(W)

    stdscr.clear()
    curses.curs_set(0)

    stdscr_y, stdscr_x = stdscr.getmaxyx()

    board_win = stdscr.subwin(SIZE, stdscr_x, 0, 0)
    log = Log()
    board = Board()
    players = [p1, p2]
    cboard = CBoard(board_win, board)
    game = Game(board, players)

    displayMenu(stdscr)
    cboard.display()

    while True:
        c = stdscr.getch()

        if 0 < c < 256:
            c = chr(c)
            if c in 'Ee':
                while not game.isOver():
                    game.step()
                    cboard.display()
            elif c in 'Ss':
                if game.log.cur == -1:
                    game.firstMove()
                else:
                    game.step()
            elif c in 'Pp':
                game.prevStep()
            elif c in 'Nn':
                game.nextStep()
            elif c in 'Qq':
                break
            elif c in 'Rr':
                game.reset()
                game.firstMove()
            else: pass

            cboard.display()
            if game.isOver():
                displayInfo(stdscr, ("%s won" % board.winPlayer))

if __name__ == '__main__':
    curses.wrapper(loop)
