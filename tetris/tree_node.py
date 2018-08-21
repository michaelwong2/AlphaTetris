from api.block import Block
from api.utils import encode_move
from api.points import *

ranker = None

# Tree node takes a 
# board
# held piece
# integer number of lines sent
# integer number of comobos so far
# integer id of last combo
# can hold bool
class Tree_node:
	def __init__(self, board, held=-1, lines_sent=0, combos_so_far=0, last_combo_id=-1, can_hold=True):

		self.board = board
		self.held = held

		self.lines_sent = lines_sent
		self.combos_so_far = combos_so_far
		self.last_combo_id = last_combo_id

		self.can_hold = can_hold

		self.moves_to_child = []
		self.children = []

		self.is_leaf = True

	@staticmethod
	def set_ranker(r):
		global ranker
		ranker = r

	def __str__(self):
		return "\n".join(["leaf: " + ("yes" if self.is_leaf else "no"), str(self.board)])

	# ACCESSOR AND MUTATOR METHODS

	# change leaf status of node
	def revoke_leaf(self):
		self.is_leaf = False

	# manage children
	def add_child(self, move, child):
		self.moves_to_child.append(move)
		self.children.append(child)

	def get_children(self):
		return self.children

	def get_child(self, i):
		return self.children[i]

	def get_rank(self):
		global ranker
		return 1 - ranker.rank(self.board, self.lines_sent)

	def get_moves_to_child(self, i):
		return self.moves_to_child[i]

	# RECURSIVE METHODS 

	# get the child which leads to the largest leaf in the tree
	# return a tuple with the moves to that child and child itself
	def get_step_towards_largest_child(self, piece):
		_, ind = self.generate_children_with_piece(piece)
		return (self.get_moves_to_child(ind), self.get_child(ind))

	# given the next piece, generate all possible children of this node if it is a leaf
	# otherwise, recurse on children till we reach a leaf
	# return type: tuple with maximum integer rank of child and index of child
	def generate_children_with_piece(self, piece):

		maximum = float('-inf')
		ind = -1

		# if not the leaf, recurse
		if not self.is_leaf:

			for i in range(len(self.children)):
				child = self.children[i]
				max_v, _ = child.generate_children_with_piece(piece)

				if max_v > maximum:
					maximum = max_v
					ind = i

			return (maximum, ind)

		# otherwise we've hit the leaf
		self.revoke_leaf()

		# in all cases, we assume there is no current piece, but there may be a held piece
		# so first generate all possible states with the current piece without holding 

		children1 = self.board.successor_states(piece)
		maximum, ind = self.make_children(children1, piece, self.held, True, False) # the next can hold because we did not hold on these

		# now we hold the piece, but only if we can hold in the first place
		if self.can_hold:

			# either there was a held piece already or not 
			# if there was a held piece, swap and execute moves and set can_hold to true for the children
			# otherwise generate one node with the current cleared, i.e. the new piece is held

			# there is a piece
			if self.held > -1:

				children2 = self.board.successor_states(self.held)
				max2, ind2 = self.make_children(children2, self.held, piece, True, True)

				if max2 > maximum:
					maximum = max2
					ind = ind2

			# hold this piece
			else:
				held_node = Tree_node(
					self.board,
					piece,
					self.lines_sent,
					self.combos_so_far,
					self.last_combo_id,
					False # can't hold the next one
				)

				self.add_child([encode_move('hold')], held_node)

				ranking = held_node.get_rank()
				if ranking > maximum:
					maximum = ranking
					ind = len(self.children) - 1

		return (maximum, ind)

	# given next possible board states and some other vars
	# generate and assign children to current node
	# return a tuple with the max child and its index
	def make_children(self, children, piece, held, next_can_hold, put_hold):

		maximum = float('-inf')
		ind = -1

		for i in range(len(children)):
			# unpack that child
			x, y, rot, moveset = children[i]

			# create new board and execute moves
			new_board = self.board.get_copy()

			new_piece = Block(piece)
			new_piece.execute_moves(moveset, self.board)
			new_piece.set(new_board)

			# calculate points
			new_lines = self.lines_sent
			combo_id = -1
			new_combos_so_far = self.combos_so_far + 1

			lines_cleared = new_board.clear_lines()

			if lines_cleared == 0:
				new_combos_so_far = 0
			else:
				is_tspin = tspin_detect(moveset)
				is_perf_clear = perf_clear_detect(new_board)
				combo_id = 1 if is_tspin else 0 if is_perf_clear else -1

				if is_tspin and is_perf_clear:
					combo_id = 2

				new_lines += next_points(self.combos_so_far - 1,
										 lines_cleared if lines_cleared != 4 else 0,
										 lines_cleared == 4,
										 is_tspin,
										 is_perf_clear,
										 combo_id == self.last_combo_id)

			# create the new node
			new_node = Tree_node(new_board,
								held,
								new_lines,
								new_combos_so_far,
								combo_id,
								next_can_hold)

			self.add_child(([encode_move('hold')] if put_hold else []) + moveset, new_node)

			ranking = new_node.get_rank()
			if ranking > maximum:
				maximum = ranking
				ind = i

		return (maximum, ind)

	def size(self):
		t = 1

		for child in self.children:
			t += child.size()

		return t
