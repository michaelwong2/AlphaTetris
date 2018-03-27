# Board class

from pgen import Piece_Generator
from block import Block
from utils import dequeue
from bmat import Board_Matrix

class Abstract_TBoard:
	def __init__(self, width=10, height=20):
		self.width = width
		self.height = height

		self.board = Board_Matrix(width, height)

		self.current_piece = None
		self.held_piece = None
		self.next_queue = []

		self.can_hold = True

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def enqueue(self, p):
		self.next_queue.append(p)

	def get_current(self):
		return self.current_piece

	def get_held(self):
		return self.held_piece

	def hold(self):

		if not self.can_hold:
			return

		h = self.held_piece
		self.held_piece = self.current_piece
		self.current_piece = h

		self.can_hold = False

	def set_piece(self):
		
		# TODO: solidify piece in resting place

		self.current_piece.set()
		self.current_piece = dequeue(self.next_queue)
		self.can_hold = True

	def check_game_over(self):

		# TODO: check that a game is over

		return False

	def make_next_move(self, policy):
		return make_choice(self.board, self.current_piece, self.held_piece, policy)

	def print_board(self):

		decoration = ''.join(['--' for i in range(self.width)])
		print decoration

		for y in range(self.height):

			line = ''

			for x in range(self.width):
				cell = self.board.lookup(x,y)

				if cell == None:
					line += '  '
				else: 
					line += cell.get_block_type() + ' '

			print line

		print decoration

	def tick(self):
		# TODO: tick
		return 



