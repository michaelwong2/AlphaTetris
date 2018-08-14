from copy import deepcopy
from api.block import Block, valid_rotations
from api.utils import encode_move
from api.bmat import Board_Matrix
from queue import Queue
from api.points import *
from collections import deque

# given a board and a piece, generate all possible board states 
# resulting from placing that piece down in a valid way
def generate_successor_states(board, piece_type):
	# number of unique rotations per piece
	r = valid_rotations(piece_type)

	# store all possible positions in a queue
	pos = deque()

	# 3D memo for later ;)
	memo = [[[0 for z in range(r)] for y in range(board.get_height())] for x in range(board.get_width())]

	# for each unique rotation
	for rotation in range(r):
		# construct a temporary piece
		temp_piece = Block(piece_type)
		temp_piece.set_rotation(board, rotation)


		# get the next offset after rotating
		sx = temp_piece.get_offset()[0]

		# for each horizontal position
		for x in range(board.get_width() - temp_piece.get_width() + 1):

			# shift the piece horizontally
			temp_piece.set_offset(x, 0)
			if temp_piece.collides(board):
				continue

			# drop
			temp_piece.drop(board)

			# get final position
			tx, ty = temp_piece.get_offset()

			# memoize
			memo[tx][ty][rotation] = 1

			#print(str(tx) + ", " + str(ty) + ", " + str(rotation))

			# encode moves
			moves = [encode_move('crot') for i in range(rotation)] + [encode_move('left') if x - sx < 0 else encode_move('right') for i in range(abs(x-sx))] + [encode_move('drop')]

			# enqueue
			pos.append((tx, ty, rotation, moves))

	# the final set to return
	children = []

	# while the queue still contains positions
	while len(pos) > 0:

		child = pos.popleft()

		# add to final bag
		children.append(child)

		x, y, rot, moves = child

		# make a block and put it into the correct place
		test_piece = Block(piece_type)
		test_piece.execute_moves(moves, board)

		o_off_x, o_off_y = test_piece.get_offset()

		# generate partial movements from this position, i.e. left, right, and all rotations
		# stored in tuples like so (dx, dy, nr)
		next_positions = [(1, 0, rot), (-1, 0, rot)] + [(0,0,i) for i in range(r)]

		# for each partial movement
		for npos in next_positions:
			# quick access variables
			dx, dy, nr = npos

			# rotate the piece for the new rotation, if possibe, else its invalid so skip
			if not test_piece.set_rotation(board, nr):
				continue

			offset = test_piece.get_offset()

			# translate the piece right or left or skip if invalid
			if (dx > 0 and not test_piece.r_translate(board)) or (dx < 0 and not test_piece.l_translate(board)):
				continue

			# apply gravity
			down = test_piece.drop(board)

			# get updated locations
			nx, ny = test_piece.get_offset()

			# check that the move was not already encoded
			if memo[nx][ny][nr] == 1:
				test_piece.dirty_reset_position(o_off_x, o_off_y, rot)
				continue

			# now encode additional movements
			# copy moves and convert drops to down movements because this is more meticulous

			nmoves = deepcopy(moves)

			# convert drops to down moves
			l = len(moves) - 1
			if moves[l] == encode_move('drop'):
				nmoves = nmoves[:l] + [encode_move('down') for i in range(y)]

			# generate additional horizontal movements
			if dx != 0:
				nmoves.append(encode_move('left') if dx == -1 else encode_move('right'))

			# generate rotation movements
			dr = nr - rot
			#print("rotations:",dr)
			if rot == 3 and nr == 0:
				nmoves += [encode_move('crot')]
			elif dr != 0:
				nmoves += [encode_move('crot') if dr > 0 else encode_move('ccrot') for i in range(abs(dr))]

			# generate additional down movements
			nmoves += [encode_move('down') for i in range(down)]

			# enqueue
			pos.append((nx, ny, nr, nmoves))

			# mark this new space as visited, too
			memo[nx][ny][nr] = 1

			# undo moves
			test_piece.dirty_reset_position(o_off_x, o_off_y, rot)

	return children

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
		return 1 - ranker.update_strat(self.board, self.lines_sent)

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
				max_v, max_i = child.generate_children_with_piece(piece)

				if max_v > maximum:
					maximum = max_v
					ind = i

			return (maximum, ind)

		# otherwise we've hit the leaf
		self.revoke_leaf()

		# in all cases, we assume there is no current piece, but there may be a held piece
		# so first generate all possible states with the current piece without holding 

		children1 = generate_successor_states(self.board, piece)
		maximum, ind = self.make_children(children1, piece, self.held, True, False) # the next can hold because we did not hold on these

		# now we hold the piece, but only if we can hold in the first place
		if self.can_hold:

			# either there was a held piece already or not 
			# if there was a held piece, swap and execute moves and set can_hold to true for the children
			# otherwise generate one node with the current cleared, i.e. the new piece is held

			# there is a piece
			if self.held > -1:

				children2 = generate_successor_states(self.board, self.held)
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





		






	
