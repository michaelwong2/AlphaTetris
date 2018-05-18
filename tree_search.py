# tree search algorithm

from api.bmat import Board_Matrix
from tree_components import Tree_node

class Tetris_Search_Tree:
	def __init__(self):
		self.last_layer = []

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

		self.root = Tree_node(board, current, held, next_queue)
		self.root.generate_children()
		self.last_layer = self.root.get_children()

		is_last_layer = False

		while not is_last_layer:

			is_last_layer = True

			l = []

			for node in self.last_layer:

				if node.is_leaf():
					l.append(node)
					continue

				node.generate_children()
				l += node.get_children()

				is_last_layer = not node.is_penultimate()

			self.last_layer = l


	def generate_next_layer(self, next_piece):

		new_layer = []

		for node in self.last_layer:

			node.enqueue(next_piece)

			node.generate_children()
			new_layer.append(node.generate_next_layer)

		self.last_layer = new_layer

	def get_last_layer(self):
		return self.last_layer

b = Board_Matrix()
t = Tetris_Search_Tree()
t.create(b, 0, -1, [4])

for c in t.get_last_layer():
	c.print_node()

# c = t.get_last_layer()
# dad = c[len(c)-1]
# dad.print_node()



