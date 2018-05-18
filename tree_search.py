# tree search algorithm

from api.bmat import Board_Matrix
from tree_components import Tree_node
from Ranker import Ranker
from test_utils import format_bmat

from api.utils import dequeue


class Tetris_Search_Tree:
	def __init__(self):
		self.ranker = Ranker()
		self.buffer = []

	def get_root(self):
		return self.root

	def size(self):
		return self.root.size()

	def next_moves(self):
		max_rank, index = self.root.get_max_child()
		moves_toward_max = self.root.get_moves_to_child(index)

		new_root = self.root.get_child(index)

		new_root.print_node()

		self.root.prune(index)
		self.root = new_root

		return moves_toward_max

	def create(self, board, current, held, next_queue):

		self.buffer = next_queue

		self.root = Tree_node(board, current, held, [dequeue(self.buffer)], 0, 0, -1, self.ranker)
		self.root.fill()

	def update(self, next_piece):
		self.buffer.append(next_piece)
		self.root.generate_next_layer(dequeue(self.buffer))

	def get_last_layer(self):
		return self.last_layer

b = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[1, 0, 0, 0, 0, 0, 1, 1, 0, 0], 
	[1, 0, 0, 1, 0, 0, 0, 1, 1, 1], 
	[0, 0, 0, 1, 1, 0, 1, 1, 1, 1]]

t = Tetris_Search_Tree()
t.create(format_bmat(b), 5, -1, [0])
print("size",t.size())

print("**************")

maxc, ind = t.get_root().get_max_child()
print("rank", maxc)
print("moves", t.next_moves())

print("**************")

t.update(2)

# for c in t.get_root().get_children():
# 	c.print_node()
# 	print(c.get_rank())

maxc, ind = t.get_root().get_max_child()
print("rank", maxc)
print("moves", t.next_moves())


