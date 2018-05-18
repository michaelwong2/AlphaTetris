# tree search algorithm

from api.bmat import Board_Matrix
from tree_components import Tree_node
from Ranker import Ranker
from test_utils import format_bmat

class Tetris_Search_Tree:
	def get_root(self):
		return self.root

	def size(self):
		return self.root.size()

	def next_moves(self):
		max_rank, index = self.root.get_max_child()
		moves_toward_max = self.root.moves_to_child(index)

		self.root = self.root.get_child(index)

		return moves_toward_max

	def create(self, board, current, held, next_queue):

		self.root = Tree_node(board, current, held, next_queue, 0, 0, -1)
		self.root.fill()

	def generate_next_layer(self, next_piece):
		self.root.generate_next_layer(next_piece)

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

for c in t.get_root().get_children():
	c.print_node()
	print(c.get_rank())

# maxc, ind = t.get_root().get_max_child()
# print("rank", maxc)
# t.get_root().get_child(ind).print_node()

# c = t.get_last_layer()
# dad = c[len(c)-1]
# dad.print_node()



