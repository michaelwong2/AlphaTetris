# tree search algorithm

from tree_components import Tree_node

class Tetris_Search_Tree:
	def __init__(self, depth):
		self.depth = depth

	def create(self, board, current, held, next_queue):
		self.root = Tree_node(board, current, held, next_queue)
