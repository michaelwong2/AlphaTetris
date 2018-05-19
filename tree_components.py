# Components of the search tree
# Tree node class

from copy import deepcopy
from api.block import Block, valid_rotations
from api.utils import dequeue, encode_move
from api.bmat import Board_Matrix
from queue import Queue
from api.points import * 
from Ranker import Ranker


def generate_successor_states(board, piece_type):
	# number of unique rotations per piece
	r = valid_rotations(piece_type)

	# store all possible positions in a queue
	pos = Queue()
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
			pos.put((tx, ty, rotation, moves))

	# the final set to return
	children = []

	# while the queue still contains positions
	while not pos.empty():

		child = pos.get()

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
			pos.put((nx, ny, nr, nmoves))

			# mark this new space as visited, too
			memo[nx][ny][nr] = 1

			# undo moves
			test_piece.dirty_reset_position(o_off_x, o_off_y, rot)

	return children


class Tree_node:
	def __init__(self, board, current, held, q, lines_sent, combos_so_far, last_combo_id, ranker, cannot_hold=False):

		self.board = board
		self.current = current
		self.held = held
		self.q = q

		self.lines_sent = lines_sent
		self.combos_so_far = combos_so_far
		self.last_combo_id = last_combo_id
		self.cannot_hold = cannot_hold

		self.ranker = ranker

		self.moves_to_child = []
		self.children = []

	def is_leaf(self):
		return self.current == -1 or self.board.check_KO()

	def is_penultimate(self):
		return len(self.q) == 0

	def size(self):
		s = 1

		for child in self.children:
			s += child.size()

		return s

	def print_node(self):
		print("Current: " + str(self.current))
		print("Held: " + str(self.held))
		print("q: " + str(self.q))
		print("lines:", self.lines_sent)
		print(self.board)

	def add_child(self, move, child):
		self.moves_to_child.append(move)
		self.children.append(child)

	def get_children(self):
		return self.children

	def get_child(self, i):
		return self.children[i]

	def get_rank(self):
		return 1 - self.ranker.update_strat(self.board, self.lines_sent)

	def get_moves_to_child(self, i):
		return self.moves_to_child[i]

	def set_current(self, c):
		self.current = c

	def enqueue(self, p):
		if self.current == -1:
			self.set_current(p)
		else:
			self.q.append(p)

	def get_board(self):
		return self.board

	# use the next piece to fill in extra children
	def generate_next_layer(self, next_piece):
		if self.is_leaf():
			self.enqueue(next_piece)
			self.generate_children()
			self.generate_held_children()
			return
		elif len(self.q) == 0:
			pass
			self.enqueue(next_piece)
			self.generate_held_children()

		for child in self.children:
			child.generate_next_layer(next_piece)

	# generate all children in the tree 
	def fill(self):
		if self.is_leaf():
			return

		self.generate_children()
		self.generate_held_children()
		for child in self.children:
			child.fill()


	# prune every child node except for node i
	def prune(self, exception):
		for i in range(exception):
			self.children[i].deep_delete()

		for i in range(exception + 1, len(self.children)):
			self.children[i].deep_delete()

	def deep_delete(self):

		del self.moves_to_child

		for child in self.children:
			child.deep_delete()
			del child

	def delete_board(self):
		del self.board

	def get_max_child(self):

		if self.is_leaf():
			# return ranking of leaf
			return (self.get_rank(), 0)

		mi = -1
		ma = 0

		for i in range(len(self.children)):
			c = self.children[i]
			max_val, ind = c.get_max_child()

			if max_val > ma:
				ma = max_val
				mi = i

		return (ma, mi)

	def generate_children(self):

		if self.is_leaf():
			return

		# only recurse with the current piece if there is one but switch pieces always
		children = generate_successor_states(self.board, self.current)
		self.make_nodes(children, self.current, self.held, self.q, False)

	def generate_held_children(self):

		# if the held piece is not the current piece, switch
		if not self.cannot_hold and self.held != self.current:

			# if there is no held piece and the queue is not empty
			# create a branch with the current piece held and the next piece dequeued
			# if self.held == -1:
			new_current = self.held 
			new_q = self.q # [1]
						   # c: 3
						   # h: -1

			if new_current == -1:
				if len(self.q) > 0:
					new_q = [] if len(self.q) < 2 else deepcopy(self.q[1:])
					new_current = self.q[0]
				else:
					return
			
			held_children = generate_successor_states(self.board, new_current)
			self.make_nodes(held_children, new_current, self.current, new_q, True)

			# new_node = Tree_node(self.board.get_copy(), self.q[0], self.current, new_q, self.lines_sent, self.combos_so_far, self.last_combo_id, self.ranker)
			# self.add_child([encode_move('hold')], new_node)

				# return

			# switch those pieces
			# held_children = generate_successor_states(self.board, self.held)
			# self.make_nodes(held_children, self.held, False)

	def make_nodes(self, children, piece_type, held_piece, q, is_held):

		for child in children:

			x, y, rot, moveset = child

			new_board = self.board.get_copy()

			new_piece = Block(piece_type)
			new_piece.execute_moves(moveset, self.board)
			new_piece.set(new_board)

			new_lines = self.lines_sent
			combo_id = -1
			new_combos_so_far = self.combos_so_far + 1

			lines_cleared = new_board.clear_lines()
			if lines_cleared == 0:
				new_combos_so_far = 0
			else:
				combo_id = 0 if tspin_detect(moveset) else 1 if perf_clear_detect(new_board) else -1
				new_lines += next_points(self.combos_so_far - 1, 
										 lines_cleared, 
										 lines_cleared == 4, 
										 combo_id == 0, 
										 combo_id == 1, 
										 combo_id == self.last_combo_id)


			nq = [] if len(q) < 2 else deepcopy(q[1:])

			new_node = Tree_node(new_board, 
								-1 if len(q) == 0 else q[0], 
								held_piece, 
								nq,
								new_lines,
								new_combos_so_far,
								combo_id,
								self.ranker,
								is_held)

			self.add_child(([encode_move('hold')] if is_held else []) + moveset, new_node)
