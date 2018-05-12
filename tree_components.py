# search tree components
from copy import deepcopy
from api.block import Block, valid_rotations
from api.utils import dequeue, encode_move, neg_inf
from api.bmat import Board_Matrix


# given a board and a piece in a specific x,y loc
# generate an array of moves corresponding to getting that piece in a certain loc
def calculate_move(board, piece):
	pass


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

	def print_node(self):
		print("Current: " + str(self.current))
		print("Held: " + str(self.held))
		print("q: " + str(len(self.q)))
		print(self.board)

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

	def get_max_child(self):

		if self.is_leaf():
			# TODO return ranking of leaf
			# something like: return Ranker.terminus_rank(self.board)
			return 1

		mi = -1
		ma = neg_inf()

		for i in range(len(self.children)):
			c = self.children[i]
			cr = c.get_max_child()

			if cr > ma:
				ma = cr
				mi = i

		return mi

	def generate_children(self):
		# only recurse with the current piece if there is one but switch pieces always
		self.generate_successor_states()

		# if there is a held piece, switch them
		if self.held > -1 and self.held != self.current:
			self.generate_successor_states(True)


	def generate_successor_states(self, is_held=False):
			# if the piece queue is empty
			empty_q = len(self.q) == 0

			current_piece = self.held if is_held else self.current
			held_piece = self.current if is_held else self.held

			for rotation in range(valid_rotations(current_piece)):

				temp_piece = Block(current_piece)
				temp_piece.set_rotation(board, rotation)

				for x in range(self.board.get_width() - temp_piece.get_width() + 1):
					for y in range(self.board.get_height() - temp_piece.get_height() + 1):

						# set the new piece offest
						temp_piece.set_offset(x, y)
						# print(str(x) + ", " + str(y))

						# if it can move down or it itersects with blocks already, continue the loop
						if temp_piece.collides(self.board) or not temp_piece.collides(self.board, 0, 1):
							continue

						# create new child with move performed
						new_board = self.board.get_copy()
						temp_piece.set(new_board)
						# print(new_board)

						# TODO: determine if we need to prune the node or not

						# create a child node
						nh = current_piece if is_held else held_piece
						if empty_q:
							new_node = Tree_node(new_board, -1, nh, [])
						else:
							nq = deepcopy(self.q)
							nc = dequeue(nq)

							new_node = Tree_node(new_board, nc, nh, nq)

						new_node.print_node()

						# calculate moves necessary
						# moveset = calculate_move(self.board, temp_piece)
						moveset = [0]

						# hold the piece if this is a hold
						if is_held:
							moveset = [encode_move('hold')] + moveset

						self.add_child(moveset, new_node)



# c = 0
# board = Board_Matrix()
# t = Tree_node(board, c, -1, [])

# t.generate_children()
# print(t.get_children())

# b = Block(0)
# print(b.get_height())
# b.set(board)
# print(board)
# print(b.collides(board))
