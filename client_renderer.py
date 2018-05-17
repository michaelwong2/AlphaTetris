# client renderer

import pygame
import sys
from random import randint

from api.bcontroller import Board_Controller
from api.utils import dequeue, decode_move, encode_move, Piece_Generator
from api.block import block_color
from api.block import Block

PIECE_W = 20
PIECE_H = 20
PIECE_MARGIN = 1

TOTAL_PIECE_WIDTH = PIECE_MARGIN + PIECE_W
TOTAL_PIECE_HEIGHT = PIECE_MARGIN + PIECE_H

TICK_DELAY = 50

GRAY = (80,80,80)

ACTIONS = {
	'LEFT':		encode_move('left'),
	'RIGHT':	encode_move('right'),
	'DOWN':		encode_move('down'),
	'UP':		encode_move('crot'),
	'SPACE':	encode_move('drop'),
	'c':		encode_move('hold'),
	'z':		encode_move('ccrot'),
	'x':		encode_move('crot'),
}

class Tetris:
	def __init__(self, width=None, height=None, policy=None):
		if height == None and width == None:
			board = Board_Controller()
		else:
			board = Board_Controller(width, height)

		self.width = board.get_width()
		self.height = board.get_height()
		self.matrix = board.get_board_matrix()

		pygame.init()
		self.screen = pygame.display.set_mode((TOTAL_PIECE_WIDTH * self.width * 3, TOTAL_PIECE_HEIGHT * self.height))

		self.pg = Piece_Generator()
		for i in range(6):
			board.enqueue(self.pg.get_next())

		board.spawn_next()

		self.board = board

		self.use_ai = policy != None
		if self.use_ai:
			self.policy = policy

		self.game_loop()

	def handle_key_event(self):

		moves = []

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				for key in ACTIONS:
					if eval("pygame.K_"+ key) == event.key:
						moves.append(ACTIONS[key])

		return moves

	def game_loop(self):

		board = self.board
		grav_rate = 200

		moves = []

		clock = pygame.time.Clock()

		tick_counter = 0

		get_moves = self.handle_key_event if not self.use_ai else self.policy

		while True:

			time = pygame.time.get_ticks()

			tick_counter += 1

			# get the next move(s)
			moves += get_moves()

			# execute move from move_queue
			if len(moves) > 0:
				next_move = dequeue(moves)
				# print('Next move: ' + decode_move(next_move))
				board.execute_move(next_move)

				if next_move == encode_move('hold'):
					board.enqueue(self.pg.get_next())

			if board.cannot_move_down():
				# reset
				board.set_current()
				board.clear_lines()

				if board.check_KO():
					break

				board.enqueue(self.pg.get_next())
				board.spawn_next()

			if tick_counter == TICK_DELAY:
				tick_counter = 0
				board.move_current_down()

			self.render()

			pygame.display.flip()
			clock.tick(60)
			prev = time

	def render(self):
		matrix = self.matrix
		w = self.width
		h = self.height

		#draw held piece
		for x in range(w):
			for y in range(1,int(h/2)):
				pygame.draw.rect(self.screen, (200,200,200),
					pygame.Rect(
						(TOTAL_PIECE_WIDTH) * x,
						(TOTAL_PIECE_HEIGHT) * y,
						PIECE_W,
						PIECE_H
					)
				)

		#locate held_piece
		held_piece = self.board.get_held()
		if held_piece != None:
			color = block_color(held_piece)
			piece = Block(held_piece)
			hx = piece.get_spawn(w)
			hy = int(h/4)

			for x in range(piece.get_width()):
				for y in range(piece.get_height()):
					if piece.loc_mat[x][y] == 1:
						pygame.draw.rect(self.screen, color,
							pygame.Rect(
							(TOTAL_PIECE_WIDTH) * (hx+x),
							(TOTAL_PIECE_HEIGHT) * (hy+y),
							PIECE_W,
							PIECE_H
							)
						)

		#draw game board
		cp = self.board.get_current()

		for x in range(w):
			for y in range(1,h):
				piece = matrix.lookup(x,y)

				if cp.intersects(x,y):
					color = cp.get_color()
				else:
					color = block_color(piece) if piece != None else GRAY

				pygame.draw.rect(self.screen, color,
					pygame.Rect(
						(TOTAL_PIECE_WIDTH) *  (w+x),
						(TOTAL_PIECE_HEIGHT) * y,
						PIECE_W,
						PIECE_H
					)
				)

		#draw next pieces
		for x in range(2*w,3*w):
			for y in range(1,h):
				pygame.draw.rect(self.screen, (200,200,200),
					pygame.Rect(
						(TOTAL_PIECE_WIDTH) * x,
						(TOTAL_PIECE_HEIGHT) * y,
						PIECE_W,
						PIECE_H
					)
				)

		q = self.board.next_queue
		print(self.matrix)
		ny = 2
		for next_piece in q[:5]:
			color = block_color(next_piece)
			piece = Block(next_piece)
			nx = piece.get_spawn(w)

			for x in range(piece.get_width()):
				for y in range(piece.get_height()):
					if piece.loc_mat[x][y] == 1:
						pygame.draw.rect(self.screen, color,
							pygame.Rect(
							(TOTAL_PIECE_WIDTH) * (2*w+nx+x),
							(TOTAL_PIECE_HEIGHT) * (ny+y),
							PIECE_W,
							PIECE_H
							)
						)
			ny += 4

t = Tetris()
