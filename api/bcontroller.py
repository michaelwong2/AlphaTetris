# Board class

from .block import Block
from .utils import dequeue, decode_move
from .bmat import Board_Matrix

class Board_Controller:
	def __init__(self, width=10, height=21):
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

	def get_board_matrix(self):
		return self.board

	# enqueue a piece into the piece queue
	def enqueue(self, t):
		self.next_queue.append(t)

	# return the current piece
	def get_current(self):
		return self.current_piece

	def set_current(self):
		self.current_piece.set(self.board)

	# return the current held piece if there is one
	def get_held(self):
		return self.held_piece

	# hold a piece
	def hold(self):
		if not self.can_hold:
			return

		h = self.held_piece
		self.held_piece = self.current_piece.get_type()
		self.current_piece = Block(h) if h != None else Block(dequeue(self.next_queue))

		self.can_hold = False

	# dequeue the next piece and place it on the board
	def spawn_next(self):
		self.current_piece = Block(dequeue(self.next_queue))
		self.can_hold = True

	# check if there is a solidified block in the top row
	# is so, that means the player was KO'd
	def check_KO(self):
		return self.board.check_KO()

	# move the current piece down
	def move_current_down(self):
		return self.current_piece.d_translate(self.board)

	def execute_move(self, move):
		if decode_move(move) != 'hold':
			self.current_piece.execute_move(move, self.board)
		else:
			self.hold()

	def cannot_move_down(self):
		return self.current_piece.collides(self.board, 0, 1)

	# clear all lines that are complete
	def clear_lines(self):
		self.board.clear_lines()

	# for debugging
	def print_board(self):

		for y in range(self.height):

			line = ''

			for x in range(self.width):
				line += self.board.lookup(x,y) + ' ' if  self.board.is_empty(x,y) else '0 '

			print(line)
