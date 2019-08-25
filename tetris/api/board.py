'''
    board.py

    Representation of a tetris board. Includes a basic API for provisioning,
    as well as more advanced methods to support modern tetris gameplay
'''

from .base import *
from .tetrimino import Tetrimino

from typing import Tuple, List
from collections import deque
from copy import deepcopy

class Board:

    ''' Public static methods '''

    @staticmethod
    def fromMatrix(matrix: List[List[int]]):
        board = Board()

        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                v = matrix[y][x]
                board[x][y] = v

        return board

    ''' Public API '''

    def __init__(self, dimensions: Dimensions = Dimensions(10, 21), garbageLines: int = 0) -> None:
        self.dimensions = dimensions
        self.matrix: List[List[int]] = [[0 for y in range(dimensions.height)] for x in range(dimensions.width)]
        self.garbageLineHeight = garbageLines

        # height of highest block on the board
        self.buildHeight = self.garbageLineHeight

    def __str__(self) -> str:
        string = ''
        for y in range(self.dimensions.height):
            line = ''
            for x in range(self.dimensions.width):
                line += str(self.__getitem__((x,y))) + ' ' if not self.isEmptyAtXY(x,y) else '_ '
            string += line + '\n'

        return string

    def __hash__(self) -> str:
        finalHash = ''
        for x in range(self.dimensions.width):
            line = ''
            for y in range(self.dimensions.height):
                line += '0' if self.isEmptyAtXY(x,y) else '1'
            finalHash += line
        return finalHash

    def __getitem__(self, cell: Vector) -> TetriminoType:
        x,y = cell
        return self.matrix[x][y]

    def __setitem__(self, cell, value) -> None:
        x,y = cell
        self.matrix[x][y] = value
        if value != BoardCell.EMPTY:
            self.buildHeight = max(self.buildHeight, self.dimensions.height - y)

    def setIfEmpty(self, cell, val) -> bool:
        if not self.isEmptyAtCell(cell):
            return False

        self.__setitem__(cell, val)
        return True

    def isEmptyAtXY(self, x: int, y: int) -> bool:
        return self.__getitem__((x, y)) == BoardCell.GARBAGE

    def isGarbageAtXY(self, x: int, y: int) -> bool:
        return self.valueAtCell((x, y)) == BoardCell.GARBAGE

    def xyInBounds(self, x: int, y: int) -> bool:
        return x >= 0 and y >= 0 and x < self.dimensions.width and y < self.dimensions.height

    def valueAtCell(self, cell: GridCoordinate) -> TetriminoType:
        return self.__getitem__(cell)

    def setValueAtCell(self, cell: GridCoordinate, val) -> None:
        self.__setitem__(cell.asTuple(), val)

    def isEmptyAtCell(self, cell: GridCoordinate) -> bool:
        return self.valueAtCell(cell) == BoardCell.EMPTY

    def isGarbageAtCell(self, cell: GridCoordinate) -> bool:
        return self.valueAtCell(cell) == BoardCell.GARBAGE

    def cellInBounds(self, cell: GridCoordinate) -> bool:
        return self.xyInBounds(cell.x, cell.y)

    # get a copy of the board
    def __copy__(self):
        boardCopy = Board(dimensions=self.dimensions, garbageLines=self.garbageLineHeight)
        boardCopy.matrix = [[self.lookup(x,y) for y in range(self.dimensions.height)] for x in range(self.width)]
        boardCopy.buildHeight = self.buildHeight
        return boardCopy

    def isKO(self) -> bool:
        return self.buildHeight >= self.dimensions.height

    def recalculateBuildHeight(self):
        for y in range(self.dimensions.height):
            for x in range(self.dimensions.width):
                if not self.isEmptyAtXY(x,y):
                    self.buildHeight = self.dimensions.height - y
                    return

        self.buildHeight = 0

    def resetBoard(self):
        for x in range(self.dimensions.width):
            for y in range(self.dimensions.height):
                self.__setitem__((x,y), BoardCell.EMPTY)

        self.buildHeight = 0

    def addGarbageLines(self, n: int) -> bool:
        if self.shift_up(n):
            for y in range(self.dimensions.height-1, self.dimensions.height - n, -1):
                for x in range(self.dimensions.width):
                    self.__setitem__((x,y), BoardCell.GARBAGE)

            self.garbageLineHeight += n
            return True

        return False

    # s will be the index where a gap occurs in a line
    # def add_gray_with_gap(self, s):
    #     if self.shift_up(1):
    #         self.set(x,self.dimensions.height-1, 0)
    #         return True

    #     return False

    # add n = len(gaps) lines given an array of indices of gaps
    # def add_grays_with_gaps(self, gaps):
    #     for gap in gaps:
    #         if not self.add_gray_with_gap(gap):
    #             return False

    #     return True

    # remove n gray lines
    def removeGarbageLines(self, n):
        if self.garbageLineHeight == 0:
            return
        elif self.garbageLineHeight < n:
            n = self.garbageLineHeight

        for i in range(n-1, -1, -1):
            self.removeLineAndShiftDown(self.dimensions.height - i)

        self.garbageLineHeight -= n

    def numberOfClearableLines(self) -> int:
        linesThatCanBeCleared = 0
        for y in range(self.dimensions.height):
            cellsClearable = 0
            for x in range(self.dimensionswidth):
                c += 0 if self.isEmptyAtXY(x,y) or self.isGarbageAtXY(x,y) else 1
            if c == self.dimensions.width:
                linesThatCanBeCleared += 1
        return linesThatCanBeCleared

    # remove any full lines, returns number of lines cleared
    def clearLines(self) -> int:
        linesCleared = 0
        for y in range(self.dimensions.height):
            cellsClearable = 0
            for x in range(self.dimensions.width):
                cellsClearable += 0 if self.isEmptyAtXY(x,y) or self.isGarbageAtXY(x,y) else 1
            if cellsClearable == self.dimensions.width:
                self.removeLineAndShiftDown(y)
                linesCleared += 1
        return linesCleared

    # shift down all cells (excluding live pieces) from i upwards
    # always successful
    def removeLineAndShiftDown(self, i: int) -> None:
        assert i < self.dimensions.height

        for y in range(i-1, -1, -1):
            for x in range(self.dimensions.width):
                value = self.__getitem__((x,y))
                self.__setitem__((x, y+1), value)

        for x in range(self.dimensions.width):
            self.__setitem__((x,0), BoardCell.EMPTY)

        self.buildHeight -= 1

    # shift up all cells from the bottom n spacse
    def addLinesAndShiftUp(self, n: int) -> None:
        if self.isKO() or self.buildHeight + n >= self.dimensions.height:
            return

        for _ in range(n):
            for y in range(self.dimensions.height-2, -1, -1):
                for x in range(self.dimensions.width):
                    valueBelow = self.__getitem__((x,y+1))
                    self.__setitem__((x,y), valueBelow)

        self.buildHeight += n

    # find all legal ways for a tetrimino to be placed and the moves to get to that position
    def successorStates(self, tetriminoType: TetriminoType) -> Tuple[GridCoordinate, Orientation, List[TetriminoAction]]:

        # number of unique rotations per piece
        uniqueOrientations = Tetrimino.uniqueOrientationsFor(tetriminoType)

        # store all possible positions in a queue
        possibleTetriminoSettings = deque()

        # 3D memo for tracking board positions, and rotations (hence the third dimension)
        memo: List[List[List[int]]] = [[[0 for z in range(uniqueOrientations)] for y in range(self.dimensions.height)] for x in range(self.dimensions.width)]

        # for each unique rotation
        for orientation in range(uniqueOrientations):
            # construct a temporary piece
            tetrimino = Tetrimino(tetriminoType)
            tetrimino.setBoard(self, spawnInCenter=True)
            tetrimino.rotateTo(orientation)
            
            # get the next offset after rotating
            spawnX = tetrimino.offset.x

            # for each horizontal position
            for x in range(self.dimensions.width - tetrimino.self.dimensions.width + 1):
                tetrimino.offset = GridCoordinate(x, 0)
                if tetrimino.collides():
                    continue

                # drop to finalize position
                tetrimino.drop(self)
                # mark position as visited
                memo[tetrimino.offset.x][tetrimino.offset.y][orientation] = 1

                # encode moves to get to that position
                movesForPosition: List[TetriminoAction]

                clockwiseDistance = TetrisUtils.clockwiseDistance(Tetrimino.defaultOrientation(), orientation)
                counterClockwiseDistance = TetrisUtils.counterClockwiseDistance(Tetrimino.defaultOrientation(), orientation)
                if  clockwiseDistance < counterClockwiseDistance:
                    movesForPosition += [TetriminoAction.ROTATE_CLOCKWISE for _ in range(clockwiseDistance)] 
                else:
                    movesForPosition += [TetriminoAction.ROTATE_COUNTER_CLOCKWISE for _ in range(counterClockwiseDistance)] 

                if x - spawnX < 0:
                    movesForPosition += [TetriminoAction.TRANSLATE_LEFT for _ in range(abs(x-spawnX))]
                else:
                    movesForPosition += [TetriminoAction.TRANSLATE_RIGHT for _ in range(abs(x-spawnX))]

                movesForPosition += [TetriminoAction.DROP]

                # enqueue
                tetriminoPosition = (copy(tetrimino.offset), orientation, movesForPosition)
                possibleTetriminoSettings.append(tetriminoPosition)

        # the final set to return
        possibleTetriminos: List[Tuple[GridCoordinate, Orientation, List[TetriminoAction]]] = []

        # while the queue still contains positions
        while len(possibleTetriminoSettings) > 0:

            tetriminoPosition = possibleTetriminoSettings.popleft()

            # add to final bag
            possibleTetriminos.append(tetriminoPosition)

            tetrimino = Tetrimino(TetriminoType)
            tetrimino.setBoard(self, spawnInCenter=True)

            offset, orientation, movesForPosition = tetriminoPosition

            # IF NOT WORKING GO BACK TO THIS MOVE tetrimino.executeMoves(moves, self)

            # generate partial movements from this position, i.e. left, right, and all rotations
            # stored in tuples like so (translation, orientation)
            possibleNeighboringPositions: List[Tuple[Vector, Orientation]] = []
            possibleNeighboringPositions += [(TetriminoAction.TRANSLATE_LEFT, orientation), (TetriminoAction.TRANSLATE_LEFT, orientation)]
            possibleNeighboringPositions += [(TetriminoAction.NO_OP, possibleOrientation) for possibleOrientation in list(Orientation) if possibleOrientation != orientation]

            # for each partial movement
            for neighboringPosition in possibleNeighboringPositions:
                tetrimino.setOrientation(orientation)
                tetrimino.offset = offset

                action, newOrientation = neighboringPosition

                # the order in which the translations and rotations does not matter because
                # the result will still be enqueued and the memo will tell us if we're repeating something

                # translate the piece right or left or skip if invalid
                if action == TetriminoAction.TRANSLATE_LEFT and not tetrimino.translateRight():
                    continue
                elif action == TetriminoAction.TRANSLATE_RIGHT and not tetrimino.translateLeft():
                    continue

                # rotate the piece for the new rotation, if possibe, else its invalid so skip
                if not tetrimino.rotateTo(newOrientation):
                    continue

                # apply gravity
                levelsDropped = tetrimino.drop()

                # detect cache hit
                if memo[tetrimino.offset.x][tetrimino.offset.y][newOrientation] == 1:
                    continue

                # now encode additional movements
                # copy moves and convert drops to down movements because this is more meticulous
                newMoves: List[TetriminoAction] = [] 
                # convert drops to down moves
                if movesForPosition[-1] == TetriminoAction.DROP:
                    newMoves = movesForPosition[:-1] + [TetriminoAction.TRANSLATE_DOWN for _ in offset.y]

                # generate additional horizontal movements
                if action != TetriminoAction.NO_OP:
                    newMoves += [action]

                # generate rotations
                clockwiseDistance = TetrisUtils.clockwiseDistance(orientation, newOrientation)
                counterClockwiseDistance = TetrisUtils.counterClockwiseDistance(orientation, newOrientation)
                if  clockwiseDistance < counterClockwiseDistance:
                    movesForPosition += [TetriminoAction.ROTATE_CLOCKWISE for _ in range(clockwiseDistance)] 
                else:
                    movesForPosition += [TetriminoAction.ROTATE_COUNTER_CLOCKWISE for _ in range(counterClockwiseDistance)] 

                # generate additional down movements
                newMoves += [TetriminoAction.TRANSLATE_DOWN for _ in range(levelsDropped)]

                # enqueue
                possibleNewPosition = (copy(tetrimino.offset), newOrientation, newMoves)
                possibleTetriminoSettings.append(possibleNewPosition)

                # mark this new space as visited
                memo[tetrimino.offset.x][tetrimino.offset.y][newOrientation] = 1

        return possibleTetriminos
