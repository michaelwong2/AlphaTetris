# Board matrix

from collections import deque
from .block import Block, valid_rotations
from .utils import encode_move
from copy import deepcopy

class Board_Matrix:
	def __init__(self, w=10, h=20, b=[], g=0, binary=False):
		self.width = w
		self.height = h

		self.mat = b if len(b) > 0 else [[0 for y in range(h)] for x in range(w)]

		self.gray_lines = g

		# use 1 and 0 to store data or use None and piece type integers
		self.store_binary = binary

		#height of highest block on the board AKA build height
		self.bheight = 0 if len(b) == 0 else self.calc_build_height()

	@staticmethod
	def from_matrix(matrix):
		b = Board_Matrix()

		for y in range(len(matrix)):
			for x in range(len(matrix[0])):
				v = matrix[y][x]

				if v != 0 and not self.store_binary:
					v = 1

				b.set(x, y, v)

		return b

	#@post: return block at coordinate. -1 for grey block. 0-6 for blocks.
	def lookup(self, x, y):
		return self.mat[x][y]

	def set(self, x, y, item):

		if item > 0:
			n = self.height - y
			self.bheight = self.bheight if n < self.bheight else n

			if self.store_binary:
				item = 1

		self.mat[x][y] = item


	def set_matrix(self, m):
		self.mat = m
		self.calc_build_height()

	def is_empty(self, x, y):
		return self.mat[x][y] == self.mat[x][y] == 0

	def is_gray(self, x, y):
		return self.mat[x][y] == -1

	def clear(self):
		for x in range(self.width):
			for y in range(self.height):
				self.set(x,y,0)

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def set_grays(self,g):
		self.gray_lines = g

	def in_bounds(self, x, y):
		return x >= 0 and y >= 0 and x < self.width and y < self.height

	def build_height(self):
		return self.bheight

	def calc_build_height(self):
		for y in range(self.height):
			for x in range(self.width):
				if not self.is_empty(x, y):
					return self.height - y

		return 0

	#@post: return a string rep of matrix
	def hash(self):
		h = ''
		for x in range(self.width):
			for y in range(self.height):
				h += '0' if self.lookup(x,y) == 0 else '1'
			h += 'b'
		return h

	# get a copy of the board
	def get_copy(self):
		c = [[self.lookup(x,y) for y in range(self.height)] for x in range(self.width)]
		return Board_Matrix(self.width, self.height, c, self.gray_lines, binary=self.store_binary)

	def check_KO(self):
		return self.build_height() >= self.height

	# add n gray lines to the bottom
	def add_grays(self, n):
		if self.shift_up(n):
			for y in range(self.height-1, self.height - n, -1):
				for x in range(self.width):
					self.set(x,y,-1)

			self.gray_lines += n
			return True

		return False

	# s will be the index where a gap occurs in a line
	def add_gray_with_gap(self, s):
		if self.shift_up(1):
			self.set(x,self.height-1, 0)
			return True

		return False

	# add n = len(gaps) lines given an array of indices of gaps
	def add_grays_with_gaps(self, gaps):
		for gap in gaps:
			if not self.add_gray_with_gap(gap):
				return False

		return True

	# remove n gray lines
	def remove_grays(self, n):

		if self.gray_lines == 0:
			return
		elif self.gray_lines < n:
			n = self.gray_lines

		for i in range(n-1, -1, -1):
			self.shift_down(self.height - i)

		self.gray_lines -= n

	# if there are any complete lines, remove them
	def clear_lines(self):
		lines_cleared = 0

		for y in range(self.height):
			c = 0

			for x in range(self.width):
				c += 0 if self.is_empty(x,y) or self.is_gray(x,y) else 1

			if c == self.width:
				self.shift_down(y)
				lines_cleared += 1

		return lines_cleared

	def resultant_points(self):
		lines_will_clear = 0
		for y in range(self.height):
			c = 0
			for x in range(self.width):
				c += 0 if self.is_empty(x,y) or self.is_gray(x,y) else 1
			if c == self.width:
				lines_will_clear += 1

		return lines_will_clear

	# shift down all cells (excluding live pieces) from i upwards
	def shift_down(self, i):

		assert i < self.height

		for y in range(i-1, -1, -1):
			for x in range(self.width):
				self.set(x,y+1, self.lookup(x,y))

		self.bheight -= 1

	# shift up all cells k <= n times
	# returns true if successful
	def shift_up(self, n):

		for i in range(n):
			if self.check_KO():
				return False

			for y in range(self.height-2, -1, -1):
				for x in range(self.width):
					self.set(x,y, self.lookup(x,y+1))

		return True

	def __str__(self):

		s = ''
		for y in range(self.height):
			line = ''
			for x in range(self.width):
				line += str(self.lookup(x,y)) + ' ' if not self.is_empty(x,y) else '_ '
			s += line + '\n'

		return s

	# given a piece, generate all possible board states 
	# resulting from placing that piece down in a valid way on this board
	def successor_states(self, piece_type):

		# number of unique rotations per piece
		r = valid_rotations(piece_type)

		# store all possible positions in a queue
		pos = deque()

		# 3D memo for later ;)
		memo = [[[0 for z in range(r)] for y in range(self.get_height())] for x in range(self.get_width())]

		# for each unique rotation
		for rotation in range(r):
			# construct a temporary piece
			temp_piece = Block(piece_type)
			temp_piece.set_rotation(self, rotation)

			# get the next offset after rotating
			sx = temp_piece.get_offset()[0]

			# for each horizontal position
			for x in range(self.get_width() - temp_piece.get_width() + 1):

				# shift the piece horizontally
				temp_piece.set_offset(x, 0)
				if temp_piece.collides(self):
					continue

				# drop
				temp_piece.drop(self)

				# get final position
				tx, ty = temp_piece.get_offset()

				# memoize
				memo[tx][ty][rotation] = 1

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
			test_piece.execute_moves(moves, self)

			o_off_x, o_off_y = test_piece.get_offset()

			# generate partial movements from this position, i.e. left, right, and all rotations
			# stored in tuples like so (dx, dy, nr)
			next_positions = [(1, 0, rot), (-1, 0, rot)] + [(0,0,i) for i in range(r)]

			# for each partial movement
			for npos in next_positions:
				# quick access variables
				dx, dy, nr = npos

				# rotate the piece for the new rotation, if possibe, else its invalid so skip
				if not test_piece.set_rotation(self, nr):
					continue

				offset = test_piece.get_offset()

				# translate the piece right or left or skip if invalid
				if (dx > 0 and not test_piece.r_translate(self)) or (dx < 0 and not test_piece.l_translate(self)):
					continue

				# apply gravity
				down = test_piece.drop(self)

				# get updated locations
				nx, ny = test_piece.get_offset()

				# check that the move was not already encoded
				if memo[nx][ny][nr] == 1:
					test_piece.dirty_reset_position(o_off_x, o_off_y, rot)
					continue

				# now encode additional movements
				# copy moves and convert drops to down movements because this is more meticulous
				nmoves = moves[:]

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
