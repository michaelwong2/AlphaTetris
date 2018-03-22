# Board class

from pgen import Piece_Generator
from block import Block
from utils import dequeue

class Streamed_Board:
	def __init__(self, width=10, height=20, current=None, nextq=[]):
		self.width = width
		self.height = height

		self.current_piece = current
		self.held_piece = None
		self.next_queue = nextq

		self.can_hold = True

		self.board = [[None for y in range(height)] for x in range(width)]

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def enqueue(self, p):
		self.next_queue.append(p)

	def hold(self):

		if not self.can_hold:
			return

		h = self.held_piece
		self.held_piece = self.current_piece
		self.current_piece = h

		self.can_hold = False

	def set_piece(self):
		
		# TODO: solidify piece in resting place

		self.current = dequeue(self.next_queue)

	def print_board(self):

		decoration = ''.join(['--' for i in range(self.width)])
		print decoration

		for y in range(self.height):

			line = ''

			for x in range(self.width):
				cell = self.board[x][y]

				if cell == None:
					line += '  '
				else: 
					line += cell.get_block_type() + ' '

			print line

		print decoration