'''
    base.py

    Enums and utils for Tetris
'''

from typing import Tuple, NewType, List
from enum import IntEnum
from random import randint, shuffle

''' Enums '''

class BoardCell(IntEnum):
    GARBAGE = -1
    EMPTY = 0
    FILLED = 1

class TetriminoType(IntEnum):
    I = 1
    J = 2
    L = 3
    O = 4
    S = 5
    T = 6
    Z = 7

class TetriminoAction(IntEnum):
    ROTATE_COUNTER_CLOCKWISE = 0
    ROTATE_CLOCKWISE = 1
    TRANSLATE_LEFT = 2
    TRANSLATE_RIGHT = 3
    TRANSLATE_DOWN = 4
    DROP = 5
    NO_OP = 6
    HOLD = 7

class Orientation(IntEnum): 
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

''' Classes '''

Color = NewType('Color', Tuple[int, int, int])
Vector = NewType('Vector', Tuple[int, int])

class GridCoordinate:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    def asTuple(self) -> Vector:
        return (self.x, self.y)

    def addVector(self, vec: Vector) -> None:
        x, y = vec
        self.x += x
        self.y += y

    def coordinateByAddingXY(self, x=0, y=0):
        return GridCoordinate(self.x + x, self.y + y)

    def coordinateByAddingVector(self, vec: Vector = (0,0)):
        x, y = vec
        return self.coordinateByAddingXY(x, y)

    def __copy__(self):
        return GridCoordinate(self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y

class Dimensions:
    def __init__(self, width=0, height=0) -> None:
        self.width = width
        self.height = height

class TetrisUtils:

    @staticmethod
    def randomTetriminoType() -> TetriminoType:
        return TetriminoType[randint(0,len(TetriminoType))]

    @staticmethod
    def clockwiseNext(direction: Orientation) -> Orientation:
        return (direction + 1) % len(Orientation)

    @staticmethod
    def counterClockwiseNext(direction: Orientation) -> Orientation:
        return (direction - 1) % len(Orientation)

    @staticmethod
    def clockwiseDistance(orientation: Orientation, orientation2: Orientation) -> int:
        return abs(orientation - orientation2)

    @staticmethod
    def counterClockwiseDistance(orientation: Orientation, orientation2: Orientation) -> int:
        mini = min(self.orientation, self.orientation2)
        maxi = max(self.orientation, self.orientation2)
        return abs((mini + len(Orientation)) - maxi)

    @staticmethod
    def randomBag() -> List[TetriminoType]:
        bag = [t for t in TetriminoType]
        shuffle(bag)
        return bag

def Log(message: str) -> None:
    print('[Tetris API]{}'.format(message))

if __name__ == '__main__':
    print(TetrisUtils.clockwiseNext(Orientation.NORTH) == 1)
    print(TetrisUtils.randomBag())
