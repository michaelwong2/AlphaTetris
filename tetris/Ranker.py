#Ranker
from random import randint

class Ranker:
    #calculate height of each column, return array
    def column_heights(self, board):
        height_list = [0 for i in range(10)]
        for x in range(board.get_width()):
            ctr = 0
            for y in range(board.get_height()):
                if not board.is_empty(x, y):
                    height_list[x] = board.get_height() - ctr
                    break
                ctr += 1
        return height_list

    #bumpiness...minimize
    def heur_bumps(self, board):
        heights = self.column_heights(board)
        # print(len(heights))
        bumpiness = 0
        for x in range(board.get_width()-1):
            bumpiness += abs(heights[x] - heights[x+1])
        return bumpiness

    #number of holes...minimize
    def pos_holes(self, board):
        holes = []
        for x in range(board.get_width()):
            ctr = 0
            for y in range(board.get_height()):
                if not board.is_empty(x, y):
                    ctr += 1
                elif board.is_empty(x, y) and ctr > 0:
                    holes.append((x, board.get_height()-y))
        return holes

    def heur_hole_depth(self, board):

        heights = self.column_heights(board)
        holes = self.pos_holes(board)
        depthSum = 0

        for i in holes:
            depthSum += heights[i[0]] - i[1]

        return depthSum

    def neighbors(self, l, x, y):

        if (x, y+1) in l:
            l.remove((x, y+1))
            self.neighbors(l, x, y+1)

        if (x+1, y) in l:
            l.remove((x+1, y))
            self.neighbors(l, x+1, y)

        if (x, y-1) in l:
            l.remove((x, y-1))
            self.neighbors(l, x, y-1)

        if (x-1, y) in l:
            l.remove((x-1, y))
            self.neighbors(l, x-1, y)

    def heur_hole_clump(self, board):
        holes = self.pos_holes(board)
        clumpHoles = 0
        for x in holes:
            clumpHoles += 1
            self.neighbors(holes, x[0], x[1])
        return clumpHoles

    def heur_avg_height(self, board):
        heights = self.column_heights(board)
        min = 20
        total = 0
        for x in heights:
            if x < min:
                min = x
            total += x
        return 16 - ((total - min) / 9)

    def rank(self, board, lines):
        a = 0.7*len(self.pos_holes(board))/180 + 0.2*self.heur_avg_height(board)/20 + 0.1*self.heur_bumps(board)/180
        return 0.4*a + 0.6*((100.0 - lines)/100.0)