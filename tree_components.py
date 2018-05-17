# search tree components
from copy import deepcopy
from api.block import Block, valid_rotations
from api.utils import dequeue, encode_move, neg_inf
from api.bmat import Board_Matrix
from queue import Queue

def dedropify(moves, y):

	l = len(moves) - 1

	moves_copy = deepcopy(moves)

	if moves[l] == encode_move('drop'):
		moves_copy = moves_copy[:l] + [encode_move('down') for i in range(y)]

	return moves_copy

def generate_successor_states(board, piece_type):

	r = valid_rotations(piece_type)

	pos = Queue()
	memo = [[[0 for z in range(r)] for y in range(board.get_height())] for x in range(board.get_width())]

	for rotation in range(r):

		temp_piece = Block(piece_type)
		temp_piece.set_rotation(board, rotation)

		sx = temp_piece.get_offset()[0]

		for x in range(board.get_width() - temp_piece.get_width() + 1):

			temp_piece.set_offset(x, 0)

			if temp_piece.collides(board): 
				continue

			temp_piece.drop(board)

			tx, ty = temp_piece.get_offset()

			memo[tx][ty][rotation] = 1
			print(str(tx) + ", " + str(ty) + ", " + str(rotation))

			moves = [encode_move('crot') for i in range(rotation)] + [encode_move('left') if x - sx < 0 else encode_move('right') for i in range(abs(x-sx))] + [encode_move('drop')]

			pos.put((tx, ty, rotation, moves))

	children = []

	print("--------------------")

	# while the queue still contains positions
	while not pos.empty():

		child = pos.get() 

		# add to final bag
		children.append(child)

		x = child[0]
		y = child[1]
		rot = child[2]
		moves = child[3]

		# make a block and put it into the correct place
		test_piece = Block(piece_type)
		test_piece.execute_moves(moves, board)
		
		# generate partial movements from this position, i.e. left, right, and all rotations
		# stored in tuples like so (dx, dy, dr)
		next_positions = [(1, 0, rot), (-1, 0, rot)] + [(0,0,i) for i in range(r)]

		# for each partial movement
		for npos in next_positions: 

			dx = npos[0]
			dy = npos[1]
			nr = npos[2]

			# if the movement is out of bounds, skip
			if not board.in_bounds(x + dx, y + dy): 
				continue

			# print("***\nRalph " + str(nr))

			# rotate the piece for the new rotation, if possibe, else its invalid so skip
			if not test_piece.set_rotation(board, nr):
				continue

			if (dx > 0 and not test_piece.r_translate(board)) or (dx < 0 and not test_piece.l_translate(board)):
				continue

			# # set the offset
			# test_piece.set_offset(dx, dy)

			# print(test_piece.loc_mat)

			# track gravity movement
			# down = 0
			# # if the piece is not valid, continue
			# if test_piece.collides(board):
			# 	continue
			# # apply gravity
			# elif not test_piece.collides(board, 0, 1):
			# 	down = test_piece.drop(board)

			# apply gravity
			down = test_piece.drop(board)

			# get updated locations
			nx, ny = test_piece.get_offset()

			# check that the move was not already encoded
			if memo[nx][ny][nr] == 1:
				continue

			print(str(nx) + ", " + str(ny) + ", " + str(nr))

			# copy moves and convert drops to down movements because this is more minute
			nmoves = dedropify(moves, y)

			# genreate additional horizontal movements
			if dx != 0:
				nmoves.append(encode_move('left') if dx == -1 else encode_move('right'))

			# generate rotations
			dr = nr - rot
			if dr != 0:
				nmoves += [encode_move('crot') if dr > 0 else encode_move('ccrot') for i in range(dr)]

			# generate additional down movements
			nmoves += [encode_move('down') for i in range(down)]

			# enqueue
			pos.put((nx, ny, nr, nmoves))

			# mark this new space as visited, too
			memo[nx][ny][nr] = 1

			test_piece.set_rotation(board, rot)
			
			if dx > 0:
				temp_piece.l_translate(board)
			elif dx < 0:
				temp_piece.r_translate(board)


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
			# TODO return ranking of leaf
			# something like: return Ranker.terminus_rank(self.board)
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
		print(children)
		self.make_nodes(children, self.current, False)

		# if there is a held piece, switch them
		if self.held > -1 and self.held != self.current:
			held_children += generate_successor_states(self.board, self.held)
			self.make_nodes(held_children, self.held, False)

	def make_nodes(self, children, piece_type, is_held):

		for child in children:

			x = child[0]
			y = child[1]
			rotation = child[2]
			moveset = child[3]

			new_board = self.board.get_copy()

			new_piece = Block(piece_type)
			new_piece.execute_moves(moveset, self.board)
			new_piece.set(new_board)

			#update lines cleared
			lines_cleared = new_board.clear_lines()

			new_q = [] if len(self.q) < 2 else deepcopy(self.q)[1:]

			new_node = Tree_node(new_board, -1 if len(self.q) == 0 else self.q[0], self.current if is_held else self.held, new_q)

			self.add_child(([encode_move('hold')] if is_held else []) + moveset, new_node)


