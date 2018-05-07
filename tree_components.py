# search tree components
from copy import deepcopy
from api.block import block, valid_rotations
from api.utils import dequeue, encode_move


# given a board and a piece in a specific x,y loc
# generate an array of moves corresponding to getting that piece in a certain loc
def calculate_move(board, piece):
	pass

# helper function to state tree BFS
# takes a board, current, held, queue, adder function, and bool
def generate_successor_states(board, current_piece, held_piece, piece_queue, add_child, is_held):




class Tree_node:
	def __init__(self, board, current, held, q):
		self.board = board
		self.current = current
		self.held = held
		self.q = q

		self.moves_to_child = []
		self.children = []

	def is_leaf(self):
		return self.current == -1

	def add_child(self, move, child):
		self.moves_to_child.append(move)
		self.children.append(child)

	def get_children(self):
		return self.children

	def get_child(self, i):
		return self.children[i]

	def moves_to_child(self, i):
		return self.moves_to_child[i]

	def set_current(self, c):
		self.current = c

	def get_board(self):
		return self.board

	def deep_delete(self):

		del move_to_child

		for child in self.children:
			child.deep_delete()
			del child

	def generate_children(self):
		# only recurse with the current piece if there is one but switch pieces always
		self.generate_successor_states(self.current, self.held, False)

		# if there is a held piece, switch them
		if self.held > -1:
			self.generate_successor_states(self.held, self.current, True)

	def generate_successor_states(self, current_piece, held_piece, is_held):
			# if the piece queue is empty
			empty_q = len(self.q) == 0

			for rotation in range(valid_rotations(current_piece)):

				temp_piece = Block(board, current_piece, rotation)

				for x in range(board.get_width() - temp_piece.get_width()):
					for y in range(board.get_height() - temp_piece.get_height()):

						# set the new piece offest
						temp_piece.set_offset(x, y)

						# if it can move down, continue the loop
						if not temp_piece.collides(0,1) and not occupied:
							continue

						# create new child with move performed
						new_board = board.get_copy()

						temp_piece.set_board(new_board)
						temp_piece.set()

						# TODO: determine if we need to prune the node or not

						# create a child node
						if empty_q:
							new_node = Tree_node(new_board, -1, held_piece, [])
						else:
							nq = deepcopy(self.q)
							new_node = Tree_node(new_board, dequeue(nq), held_piece, nq)

						# calculate moves necessary
						moveset = calculate_move(board, temp_piece)

						# hold the piece if this is a hold
						if is_held:
							moveset = [encode_move('hold')] + moveset

						self.add_child(moveset, new_node)

						# reset temp piece to be a new block
						temp_piece = Block(board, current_piece, rotation)
