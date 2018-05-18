# Components of the search tree
# Tree node class

from copy import deepcopy
from api.block import Block, valid_rotations
from api.utils import dequeue, encode_move, neg_inf
from api.bmat import Board_Matrix
from queue import Queue

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
	i = 0

	# while the queue still contains positions
	while not pos.empty():
		i += 1
		child = pos.get()
		#print("Child",i,":",child)

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

			# print(str(nx) + ", " + str(ny) + ", " + str(nr))

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
			# return ranking of leaf
			# return ranker.rank(self.board)
			return 1

		mi = -1
		ma = neg_inf()

		for i in range(len(self.children)):
			c = self.children[i]
			cr = c.get_max_child()

			if cr > ma:
				ma = cr
				mi = i

		return ma

	def generate_children(self):
		# only recurse with the current piece if there is one but switch pieces always
		children = generate_successor_states(self.board, self.current)
		self.make_nodes(children, self.current, False)

		# if the held piece is not the current piece, switch
		if self.held != self.current:

			# if there is no held piece and the queue is not empty
			# create a branch with the current piece held and the next piece dequeued
			if self.held == -1:
				if len(self.q) == 0:
					return
				else:
					new_q = [] if len(self.q) < 2 else deepcopy(self.q)[1:]
					new_node = Tree_node(self.board.get_copy(), self.q[0], self.current, new_q)
					self.add_child([encode_move('hold')], new_node)

			# switch those pieces
			held_children += generate_successor_states(self.board, self.held)
			self.make_nodes(held_children, self.held, False)

	def make_nodes(self, children, piece_type, is_held):

		for child in children:

			x, y, rot, moveset = child

			new_board = self.board.get_copy()

			new_piece = Block(piece_type)
			new_piece.execute_moves(moveset, self.board)
			new_piece.set(new_board)

			#update lines cleared
			lines_cleared = new_board.clear_lines()

			new_q = [] if len(self.q) < 2 else deepcopy(self.q)[1:]

			new_node = Tree_node(new_board, -1 if len(self.q) == 0 else self.q[0], self.current if is_held else self.held, new_q)

			self.add_child(([encode_move('hold')] if is_held else []) + moveset, new_node)
