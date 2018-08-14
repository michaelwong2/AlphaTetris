# tree search algorithm

from api.bmat import Board_Matrix
from tree_components import Tree_node
from Ranker import Ranker
from collections import deque

class Tetris_Search_Tree:
	# create the tree and give it a list of starting pieces and the depth parameter
	def __init__(self, board, initial_pieces, k=1):	

		starting_set = initial_pieces[:k]
		self.buffer = deque(initial_pieces[k:])

		# set the ranker
		Tree_node.set_ranker(Ranker())
		
		# create default root
		self.root = Tree_node(board=board)

		# generate a new layer for each piece in the starting set
		for i in range(k):
			self.root.generate_children_with_piece(starting_set[i])

	def get_root(self):
		return self.root

	def size(self):
		return self.root.size()

	# get the next moves, generate another layer and 
	def next_moves(self):

		if(len(self.buffer) == 0):
			return []

		moves, next_child = self.root.get_step_towards_largest_child(self.buffer.popleft())

		self.root = next_child

		return moves

	# add a single piece or a batch
	def enqueue(self, next_piece):
		if type(next_piece) is list:
			self.buffer.extend(next_piece)
		elif type(next_piece) is int:
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

# t = Tetris_Search_Tree(Board_Matrix.from_matrix(b), [0, 1, 3, 1, 5])
# print("size", t.size())

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
# 	print(c)
# 	print("dADd-----------")
# 	for cc in c.get_children():
# 		print(cc)

# 	print("---------------")
# 	print(c.get_rank())



# maxc, ind = t.get_root().get_max_child()
# print("rank", maxc)
# print("moves", t.next_moves())


