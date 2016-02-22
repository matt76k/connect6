SIZE = 21
B, W, Empty, Edge = 1, -1, 0, 2

class Board:

    def putDown(self, x, y, stone):
        self.board[x][y] = stone

    def isFull(self):
        return all([i.count(Empty) == 0 for i in self.board])

    def isGameOver(self):
        for i in self.__getHorizontal() + self.__getVertical() + self.__getDiagonalUp() + self.__getDiagonalDown():
            if self.__check(i):
                return True
        return False

    def __clearBoard(self):
        self.board = [[Empty for i in range(SIZE)] for j in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                if i == 0 or i == 20 or j == 0 or j == 20:
                    self.board[i][j] = Edge

    def __str__(self):
        def stone(i):
            if i == B:
                return "o"
            elif i == W:
                return "x"
            elif i == Empty:
                return "."
            else:
                return "+"

        return "\n".join(["".join([stone(j) for j in i]) for i in self.board])

    def __check(self, line):
        b = Edge
        n = 0

        for i in line:
            if Empty == i:
                n = 0
            elif b == i:
                n += 1
            else:
                n = 1
            if n == 6:
                self.winPlayer = "Black" if i == B else "White"
                return True
            b = i
        return False

    def __getHorizontal(self):
        return [i[1:] for i in self.board[1:SIZE - 1]]

    def __getVertical(self):
        return [[self.board[j][i] for j in range(1, SIZE)] for i in range(1, SIZE - 1)]

    def __getDiagonal(self, ix, iy, dx, dy):
        line = []
        x, y = ix, iy
        s = self.board[x][y]
        while s != Edge:
            line.append(s)
            x += dx
            y += dy
            s = self.board[x][y]
        return line

    def __getDiagonalUp(self):
        lines = []
        for i in range(6, SIZE - 1):
            lines.append(self.__getDiagonal(i, 1, -1, 1))
        for i in range(2, SIZE - 6):
            lines.append(self.__getDiagonal(SIZE - 2, i, -1, 1))
        return lines

    def __getDiagonalDown(self):
        lines = []
        for i in range(1, SIZE - 6):
           lines.append(self.__getDiagonal(i, 1, 1, 1))
        for i in range(2, SIZE - 6):
            lines.append(self.__getDiagonal(1, i, 1, 1))
        return lines

    def __init__(self):
        self.__clearBoard()
        self.winPlayer = "Draw"

if __name__=='__main__':
    b = Board()
    print(b)
