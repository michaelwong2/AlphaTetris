# tree search algorithm

from api.bmat import Board_Matrix
from tree_components import Tree_node
from Ranker import Ranker
from test_utils import format_bmat

from api.utils import dequeue

class Tetris_Search_Tree:
	def __init__(self, depth=1):
		self.depth = depth
		self.ranker = Ranker()
		self.buffer = []

	def get_root(self):
		return self.root

	def size(self):
		return self.root.size()

	def next_moves(self):

		if self.root.is_leaf():
			return -1

		max_rank, index = self.root.get_max_child()
		moves_toward_max = self.root.get_moves_to_child(index)

		new_root = self.root.get_child(index)

		self.root.prune(index)
		self.root = new_root

		if len(self.buffer) > 1:
			self.root.generate_next_layer(dequeue(self.buffer))

		# print(moves_toward_max)

		return moves_toward_max

	def create(self, board, starting_pieces):

		# print(starting_pieces)

		self.buffer = starting_pieces[1:]

		starting = []

		for i in range(self.depth):
			starting.append(dequeue(self.buffer))

		self.create_from_position(board, starting_pieces[0], -1, starting)

	def create_from_position(self, board, current, held, next_queue):
		self.root = Tree_node(board, current, held, next_queue, 0, 0, -1, self.ranker)
		self.root.fill()

	def enqueue(self, next_piece):

		if len(self.buffer) == 0:
			self.root.generate_next_layer(next_piece)
		else:
			self.buffer.append(next_piece)
		

# b = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# t = Tetris_Search_Tree()
# t.create(format_bmat(b), [0, 1, 3, 1, 5])
# print("size",t.size())

# print("**************")

# maxc, ind = t.get_root().get_max_child()
# print("rank", maxc)
# print("moves", t.next_moves())

# maxc, ind = t.get_root().get_max_child()
# print("rank", maxc)
# print("moves", t.next_moves())

# maxc, ind = t.get_root().get_max_child()
# print("rank", maxc)
# print("moves", t.next_moves())

# for c in t.get_root().get_children():
# 	c.print_node()
# 	print(c.get_rank())



# maxc, ind = t.get_root().get_max_child()
# print("rank", maxc)
# print("moves", t.next_moves())


