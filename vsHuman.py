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
    scr.move(SIZE + 1, 0)
    scr.clrtoeol()
    scr.addstr(SIZE + 1, 0, s)
    scr.refresh()

def displayPos(scr, y, x):
    scr.move(SIZE, 0)
    scr.clrtoeol()
    scr.addstr(SIZE, 0, "pos:(%s, %s)" % (y, x))
    scr.move(y, x)
    scr.refresh()

def displayMenu(scr):
    scr.addstr(SIZE + 2, 0, "Q) Quit,  Space) put stone, P) Prev, N) Next")

def loop(stdscr):
    stdscr.clear()
    stdscr_y, stdscr_x = stdscr.getmaxyx()

    board_win = stdscr.subwin(SIZE, stdscr_x, 0, 0)
    log = Log()
    board = Board()

    # if you want to play first, you set human to 0. otherwise you set human to 1
    human = 0
    p1, p2 = RandomPlayer(B), RandomPlayer(W)

    players = [p1, p2]
    cboard = CBoard(board_win, board)
    game = Game(board, players)

    xpos, ypos = cboard.X//2 + 1, cboard.Y//2 + 1

    displayMenu(stdscr)

    moves = []

    while True:
        stdscr.move(ypos, xpos)
        displayPos(stdscr, ypos, xpos)

        if human != 0 and game.log.cur == -1:
            game.firstMove()
            cboard.display()
            stdscr.move(ypos, xpos)

        c = stdscr.getch()

        if 0 < c < 256:
            c = chr(c)
            if c in ' \n':
                if game.isOver() or game.board.board[ypos][xpos] != Empty:
                    continue
                elif human == 0 and game.log.cur == -1:
                    game.board.putDown(ypos, xpos, players[human].stone)
                    game.updateTurn()
                    game.log.add([(ypos, xpos)])
                    cboard.display()
                    game.step()

                elif len(moves) == 1:
                    moves.append((ypos, xpos))
                    game.board.putDown(ypos, xpos, players[human].stone)
                    game.updateTurn()
                    game.log.add(moves)
                    moves = []
                    game.step()
                else:
                    moves.append((ypos, xpos))
                    game.board.putDown(ypos, xpos, players[human].stone)
            elif c in 'Pp':
                game.prevStep()
                game.prevStep()
            elif c in 'Nn':
                game.nextStep()
                game.nextStep()
            elif c in 'Qq':
                break
            else: pass

            cboard.display()
            if game.isOver():
                displayInfo(stdscr, ("%s won" % board.winPlayer))

        elif c == curses.KEY_UP and ypos > 1:           ypos -= 1
        elif c == curses.KEY_DOWN and ypos < cboard.Y:  ypos += 1
        elif c == curses.KEY_LEFT and xpos > 1:         xpos -= 1
        elif c == curses.KEY_RIGHT and xpos < cboard.X: xpos += 1
        else: pass

if __name__ == '__main__':
    curses.wrapper(loop)
