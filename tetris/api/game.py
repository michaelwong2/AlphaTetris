'''
    game.py
'''

from .base import *
from .board import Board
from .tetrimino import Tetrimino

import pygame, sys
from random import randint
from copy import copy, deepcopy
from collections import deque
from typing import List, Tuple

''' Private render variables'''

# board
_boardDimensions = Dimensions(10, 21)

# cell
_cellDimensions = Dimensions(20, 20)
_cellBorderSize = 1
_cellBGColor = (80, 80, 80)
_garbageCellColor = (210,210,210)

# tetrimino suspended view, e.g. held and in-queue
_tetriminoSuspendedViewDimensionsWidth = _cellDimensions.width * 5
_tetriminoViewBGColor = (200, 200, 200)

''' Private game logic variables'''

_msPerTick = 50
_gravityEffectMS = 200

keyMap = {
    'z':        TetriminoAction.ROTATE_COUNTER_CLOCKWISE,
    'x':        TetriminoAction.ROTATE_CLOCKWISE,
    'UP':       TetriminoAction.ROTATE_CLOCKWISE,
    'LEFT':     TetriminoAction.TRANSLATE_LEFT,
    'RIGHT':    TetriminoAction.TRANSLATE_RIGHT,
    'DOWN':     TetriminoAction.TRANSLATE_DOWN,
    'SPACE':    TetriminoAction.DROP,
    'c':        TetriminoAction.HOLD
}

class Tetris:
    def __init__(self):
        boardWidth = _cellDimensions.width * _boardDimensions.width
        boardHeight = _cellDimensions.height * _boardDimensions.height
        queueViewWidth = _tetriminoSuspendedViewDimensionsWidth

        pygame.init()
        self.screen = pygame.display.set_mode((boardWidth + (_tetriminoSuspendedViewDimensionsWidth*2), boardHeight))

        def listenForUserInput(a, b, c, d) -> List[TetriminoAction]:
            moves = []

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    for key in keyMap:
                        if eval("pygame.K_"+ key) == event.key:
                            moves.append(keyMap[key])

            return moves

        self.board = Board()
        self.queue = deque()
        self.held: Tetrimino = None
        self.current: Tetrimino = None

        self.gameLoop(listenForUserInput)
    
    def gameLoop(self, listenForEvents):
        clock = pygame.time.Clock()
        ms = 0
        eventQueue = deque()

        def dequeue() -> None:
            if len(self.queue) == 0:
                self.queue = deque(TetrisUtils.randomBag())

            self.current = Tetrimino(self.queue.popleft())
            self.current.setBoard(self.board)
 
        def reset() -> bool:
            self.current.commit()
            self.board.clearLines()

            if self.board.isKO():
                return False

            dequeue()
            return True

        dequeue()
        while True:
            time = pygame.time.get_ticks()
            ms += 1

            # listen for the next move(s)
            eventQueue.extend(listenForEvents(self.board, self.current, self.held, self.queue))
            if len(eventQueue) > 0:
                nextMove = eventQueue.popleft()
                self.current.executeMove(nextMove)

                if nextMove == TetriminoAction.HOLD:
                    self.held = self.current
                    dequeue()
                elif nextMove == TetriminoAction.DROP:
                    if not reset():
                        break 
                    else:
                        # moves.extend(get_moves())
                        ms = 0
                        continue
                elif nextMove == TetriminoAction.ROTATE_COUNTER_CLOCKWISE:
                    self.current.rotate(clockwise=False)
                elif nextMove == TetriminoAction.ROTATE_CLOCKWISE:
                    self.current.rotate(clockwise=True)                    
                elif nextMove == TetriminoAction.TRANSLATE_LEFT:
                    self.current.translateLeft()
                elif nextMove == TetriminoAction.TRANSLATE_RIGHT:
                    self.current.translateRight()
                elif nextMove == TetriminoAction.TRANSLATE_DOWN:
                    self.current.translateDown()

                ms = 0

            if ms == _msPerTick:
                ms = 0

                # the tick has ended so translate the current piece down
                # if it has hit another tetrimino or the bottom, reset
                if not self.current.translateDown():
                    if not reset():
                        break
                    else:
                        # moves.extend(get_moves())
                        pass

            self.render(self.board, self.current, self.held, self.queue)
            pygame.display.flip()
            clock.tick(60)

    def drawRect(self, x:int, y:int, w:int, h:int, color:Color) -> None:
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, w, h))

    def drawCell(self, x:int, y:int, color:Color = _cellBGColor) -> None:
        self.drawRect(x, y, _cellDimensions.width, _cellDimensions.height, color)
   
    def render(self, board: Board, currentTetrimino: Tetrimino, heldTetrimino: TetriminoType, nextTetriminos: List[TetriminoType]) -> None:
        width = _boardDimensions.width
        height = _boardDimensions.height

        # held tetrimino
        if heldTetrimino is not None:
            color = Tetrimino.colorOf(heldTetrimino)
            heldDimensions = Tetrimino.dimensionsOf(heldTetrimino)
            renderedWidth = (_cellDimensions.width * heldDimensions.width) + (_cellBorderSize * (heldDimensions.width-1))
            renderedHeight = (_cellDimensions.height * heldDimensions.height) + (_cellBorderSize * (heldDimensions.height-1))

            offset = GridCoordinate()
            offset.x = (_tetriminoSuspendedViewDimensionsWidth - renderedWidth) // 2
            offset.y = 50

            heldShape = Tetrimino.shapeOf(heldTetrimino)
            
            for x in range(heldDimensions.width):
                for y in range(heldDimensions.height):
                    if heldShape[x][y] == BoardCell.FILLED:
                        self.drawCell(offset.x + (_cellDimensions.width + _cellBorderSize)*x, 
                                      offset.y + (_cellDimensions.width + _cellBorderSize)*y)

        # board
        offset = GridCoordinate()
        offset.x = _tetriminoSuspendedViewDimensionsWidth
        offset.y = 0

        for x in range(width):
            for y in range(height):
                cell = board[x,y]
                color = _cellBGColor
                if currentTetrimino.isPresentAtCell(GridCoordinate(x,y)):
                    color = Tetrimino.colorOf(currentTetrimino.tetriminoType)
                elif cell == BoardCell.GARBAGE:
                    color = _garbageCellColor

                self.drawCell(offset.x + (_cellDimensions.width + _cellBorderSize)*x, offset.y + (_cellDimensions.width + _cellBorderSize)*y)
