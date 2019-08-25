'''
    tetrimino.py

    Representation of a Tetrimino. Types can be added and customized. Supports wall kicks for 
    t-spins and other modern tetris game features
'''

from .base import *

from typing import Tuple, List
from random import randint
from math import floor, ceil
from copy import copy

class TETRIMINO_GUIDE: 
    def __init__(self, shape: List[List[int]], uniqueRotations: int, clockwiseTransitionVectors: List[Vector], counterClockwiseTransitionVectors: List[Vector], color: Color):
        self.shape = shape
        self.uniqueRotations = uniqueRotations
        self.clockwiseTransitionVectors = clockwiseTransitionVectors
        self.counterClockwiseTransitionVectors = counterClockwiseTransitionVectors
        self.color = color

TETRIMINOS_CONFIG = {
    TetriminoType.I: TETRIMINO_GUIDE([[1],
                                        [1],
                                        [1],
                                        [1]],
                                        uniqueRotations = 2,
                                        clockwiseTransitionVectors = [(-1,1),(2,-1),(-2,2),(1,-2)],
                                        counterClockwiseTransitionVectors = [(-2,1),(2,-2),(-1,2),(1,-1)],
                                        color = (31,185,253)),
    TetriminoType.J: TETRIMINO_GUIDE([[1,1],
                                        [0,1],
                                        [0,1]],
                                        uniqueRotations = 4,
                                        clockwiseTransitionVectors = [(0,0),(1,0),(-1,1),(0,-1)],
                                        counterClockwiseTransitionVectors = [(-1,0),(1,-1),(0,1),(0,0)],
                                        color = (24,73,196)),
    TetriminoType.L: TETRIMINO_GUIDE([[0,1],
                                        [0,1],
                                        [1,1]],
                                        uniqueRotations = 4,
                                        clockwiseTransitionVectors = [(0,0),(1,0),(-1,1),(0,-1)],
                                        counterClockwiseTransitionVectors = [(-1,0),(1,-1),(0,1),(0,0)],
                                        color = (255,120,10)),
    TetriminoType.O: TETRIMINO_GUIDE([[1,1],
                                        [1,1]],
                                        uniqueRotations = 1,
                                        clockwiseTransitionVectors = [(0,0),(0,0),(0,0),(0,0)],
                                        counterClockwiseTransitionVectors = [(0,0),(0,0),(0,0),(0,0)],
                                        color = (240,182,45)),
    TetriminoType.S: TETRIMINO_GUIDE([[0,1],
                                        [1,1],
                                        [1,0]],
                                        uniqueRotations = 2,
                                        clockwiseTransitionVectors = [(0,0),(1,0),(-1,1),(0,-1)],
                                        counterClockwiseTransitionVectors = [(-1,0),(1,-1),(0,1),(0,0)],
                                        color = (130,209,65)),
    TetriminoType.T: TETRIMINO_GUIDE([[0,1],
                                        [1,1],
                                        [0,1]],
                                        uniqueRotations = 4,
                                        clockwiseTransitionVectors = [(0,0),(1,0),(-1,1),(0,-1)],
                                        counterClockwiseTransitionVectors = [(-1,0),(1,-1),(0,1),(0,0)],
                                        color = (212,44,155)),
    TetriminoType.Z: TETRIMINO_GUIDE([[1,0],
                                        [1,1],
                                        [0,1]],
                                        uniqueRotations = 2,
                                        clockwiseTransitionVectors = [(0,0),(1,0),(-1,1),(0,-1)],
                                        counterClockwiseTransitionVectors = [(-1,0),(1,-1),(0,1),(0,0)],
                                        color = (248,58,93))
}

class Tetrimino:

    ''' Public static methods '''

    @staticmethod
    def colorOf(tetriminoType: TetriminoType) -> Color:
        return TETRIMINOS_CONFIG[tetriminoType].color

    @staticmethod
    def randomTetrimino():
        return Tetrimino(TetrisUtils.randomTetriminoType())

    @staticmethod
    def uniqueOrientationsFor(tetriminoType: TetriminoType) -> int:
        return TETRIMINOS_CONFIG[tetriminoType].uniqueOrientations

    @staticmethod
    def defaultOrientation() -> Orientation:
        return Orientation.NORTH

    @staticmethod
    def shapeOf(tetriminoType: TetriminoType) -> Dimensions:
        return TETRIMINOS_CONFIG[tetriminoType].shape

    @staticmethod
    def dimensionsOf(tetriminoType: TetriminoType) -> Dimensions:
        shape = Tetrimino.shapeOf(tetriminoType)
        return Dimensions(len(shape), len(shape[0]))

    ''' Public API '''

    def __init__(self, tetriminoType: TetriminoType):
        self.tetriminoType = tetriminoType
        self.orientation = Tetrimino.defaultOrientation()
        self.shape = Tetrimino.shapeOf(tetriminoType)
        self.dimensions = Tetrimino.dimensionsOf(tetriminoType)

        self.board = None
        self.spawn = GridCoordinate()
        self.offset = GridCoordinate()

    def setBoard(self, board, spawnInCenter: bool = True) -> None:
        self.board = board
        if spawnInCenter:
            self.spawn = GridCoordinate(floor(board.dimensions.width / 2) - ceil(self.dimensions.width/2), 0)
            self.offset = copy(self.spawn)

    def commit(self) -> bool:
        assert self.board is not None
        encoding = self.tetriminoType
        for x in range(self.dimensions.width):
            for y in range(self.dimensions.height):
                if self.shape[x][y]:
                    if not self.board.setIfEmpty(self.offset.coordinateByAddingVector((x, y)), encoding):
                        return False
        return True

    def uniqueOrientations(self) -> int:
        return Tetrimino.uniqueOrientationsFor(self.tetriminoType)

    def __str__(self) -> str:
        return "<Tetrimino type={} offset=({},{})>".format(self.tetriminoType, self.offset.x, self.offset.y)

    def __copy__(self):
        tetrimino = Tetrimino(self.tetriminoType)
        tetrimino.orientation = self.orientation
        return tetrimino

    # return True if the coordinate intersects with part of the piece
    def isPresentAtCell(self, cell: GridCoordinate) -> bool:
        withinLeftBounds: bool = cell.x >= self.offset.x
        withinRightBounds: bool = cell.x < (self.offset.x + self.dimensions.width)
        withinTopBounds: bool = cell.y >= self.offset.y
        withinBottomBounds: bool = cell.y < (self.offset.y + self.dimensions.height)

        if withinLeftBounds and withinRightBounds and withinTopBounds and withinBottomBounds:
            return self.shape[cell.x - self.offset.x][cell.y - self.offset.y] == BoardCell.FILLED

        return False

    def translateLeft(self) -> bool:
        return self._translateWithVector((-1, 0))

    def translateRight(self) -> bool:
        return self._translateWithVector((1, 0))

    def translateDown(self):
        return self._translateWithVector((0, 1))

    def drop(self, board) -> int:
        d = 0
        while self.translateDown():
            d += 1
        return d

    def rotateTo(self, targetOrientation: Orientation) -> bool:
        clockwiseDistance = TetrisUtils.clockwiseDistance(self.orientation, targetOrientation)
        counterClockwiseDistance = TetrisUtils.counterClockwiseDistance(self.orientation, targetOrientation)

        for _ in min(clockwiseDistance, counterClockwiseDistance):
            if _rotateOnce(clockwise = clockwiseDistance < counterClockwiseDistance):
                return False

        return True

    def rotate(self, clockwise: bool = True) -> bool:
        return self._rotateOnce(self, clockwise, enableWallKicks=True)

    # not recommended unless ignoring the board
    def setOrientation(self, targetOrientation: Orientation) -> None:
        for _ in range(TetrisUtils.clockwiseDistance(self.orientation, targetOrientation)):
            self._rotateOnce(clockwise=True, enableWallKicks=False)

    def collides(self, vector: Vector) -> bool:
        assert self.board is not None
        dx, dy = vector
        for innerX in range(self.dimensions.width):
            for innerY in range(self.dimensions.height):
                if self.shape[innerX][innerY] == BoardCell.EMPTY:
                    continue
                elif innerY > 0 and self.shape[innerX][innerY-1] == BoardCell.FILLED:
                    continue

                x = self.offset.x + innerX
                y = self.offset.y + innerY

                if not self.board.xyInBounds(x + dx, y + dy) or not self.board.isEmptyAtXY(x + dx, y + dy):
                    return True

        return False

    def hasClearOverhead(self):
        assert self.board is not None
        for innerX in range(self.dimensions.width):
            for innerY in range(self.dimensions.height):
                if self.shape[innerX][innerY] == BoardCell.EMPTY:
                    continue

                x = self.offset.x + innerX
                y = self.offset.y + innerY - 1

                while not self.board.xyInBounds(x,y):
                    if not self.board.isEmptyAtXY(x,y):
                        return False
                    y -= 1

        return True

    def executeMove(self, move: TetriminoAction) -> bool:
        if move == TetriminoAction.ROTATE_COUNTER_CLOCKWISE:
            return self._rotateOnce(clockwise=False)
        elif move == TetriminoAction.ROTATE_CLOCKWISE:
            return self._rotateOnce(clockwise=True)
        elif move == TetriminoAction.TRANSLATE_LEFT:
            return self.translateLeft()
        elif move == TetriminoAction.TRANSLATE_RIGHT:
            return self.translateRight()
        elif move == TetriminoAction.TRANSLATE_DOWN:
            return self.translateDown()
        elif move == TetriminoAction.DROP:
            self.drop()
            return True
        else:
            Log("Cannot perform action")
            return False

    def executeMoves(self, moves: List[TetriminoAction]) -> bool:
        for move in moves:
            if not self.executeMove(move):
                return False

        return True

    ''' Private API '''
  
    # If possible translates the tetrimino in the Orientation of the vector given, returns bool: success vs failure
    def _translateWithVector(self, vector: Vector) -> bool:
        if not self.collides(vector):
            self.offset.addVector(vector)
            return True

        return False

    def _rotateOnce(self, clockwise: bool = True, enableWallKicks: bool = False) -> bool:
        newShape: List[List[int]] = []
        newOrientation = TetrisUtils.clockwiseNext(self.orientation) if clockwise else TetrisUtils.counterClockwiseNext(self.orientation)
        newDimensions = Dimensions()
        translationVector: Vector = (0,0)

        if clockwise:
            newShape = [[self.shape[x][y] for x in range(self.dimensions.width)] for y in range(self.dimensions.height-1, -1, -1)]
            translationVector = crot_translations[tetriminoType][newOrientation]
        else:
            newShape = [[self.shape[x][y] for x in range(self.dimensions.width-1,-1,-1)] for y in range(self.dimensions.height)]
            translationVector = ccrot_translations[tetriminoType][newOrientation]

        newOffset: GridCoordinate = GridCoordinate(self.offset.x + translationVector.x, self.offset.y + translationVector.y)
        newDimensions.width = len(newShape)
        newDimensions.height = len(newShape[0])

        if enableWallKicks:
            wallKickVector = self._computeWallKickVector(self, newShape, newDimensions, newOffset)

            if wallKickVector != (0,0): 
                newOffset.addVector(wallKickVector)

                if self._computeWallKickVector(self, newShape, newDimensions, newOffset) != (0,0):
                    return False

        self.offset = newOffset
        self.shape = newShape
        self.orientation = newOrientation
        self.dimensions = newDimensions

        return True

    def _computeWallKickVector(self, shape: List[List[int]], dimensions: Dimensions, newOffset: GridCoordinate) -> Vector:
        assert self.board is not None
        for innerX in range(dimensions.width):
            for innerY in range(dimensions.height):

                if shape[innerX][innerY] == BoardCell.EMPTY:
                    continue

                x = newOffset.x + innerX
                y = newOffset.y + innerY

                if not self.board.xyInBounds(x,y) or not self.board.isEmptyAtXY(x,y):
                    if innerX == 0:
                        return (1, 1)
                    else:
                        return (-1, 1)

        return (0, 0)
