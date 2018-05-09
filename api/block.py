# Block class

from random import randint
import math

block_types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

block_mats = [

	[[1],
	 [1],
	 [1],
	 [1]],

	[[1,1],
	 [0,1],
	 [0,1]],

	[[0,1],
	 [0,1],
	 [1,1]],

	[[1,1],
	 [1,1]],

	[[0,1],
	 [1,1],
	 [1,0]],

	[[0,1],
	 [1,1],
	 [0,1]],

	[[1,0],
	 [1,1],
	 [0,1]]
]

vrots = [2,4,4,1,2,4,2]

colors = [
	(31,185,253),
	(24,73,196),
	(255,120,10),
	(240,182,45),
	(130,209,65),
	(212,44,155),
	(248,58,93)
]

def block_color(t):
	if t <= -1:
		return (200,200,200)
	else:
		return colors[t]

def valid_rotations(t):
	return vrots[t]

# initialize a Block object with a board, a type (int, 0-6), rotation (int, 0-3) and offset (tuple x,y)
# or only include the board for a random block with default rotation and default position
class Block:
	def __init__(self, t=None, r=0):

		self.t = t if t != None else randint(0,6)
		self.rot = r

		self.loc_mat = block_mats[self.t]

		self.inner_width = len(self.loc_mat)
		self.inner_height = len(self.loc_mat[0])

		self.set_offset(self.get_spawn())

	def set(self, board):
		try:
			for x in range(self.inner_width):
				for y in range(self.inner_height):
					if self.loc_mat[x][y] == 1:
						board.set(self.off_x + x, self.off_y + y, self.t)
		except:
			print("error ...")

			for x in range(self.inner_width):
				for y in range(self.inner_height):
					if self.loc_mat[x][y] == 1:
						print("accessing " + str(self.off_x + x) + ", " + str(self.off_y + y))
						board.set(self.off_x + x, self.off_y + y, self.t)

	def get_spawn(self, width=10):
		return (math.floor(width / 2) - math.ceil(self.inner_width/2), 0)

	def get_type(self):
		return self.t

	def get_width(self):
		return len(self.loc_mat)

	def get_height(self):
		return len(self.loc_mat[0])

	def get_offset(self):
		return (self.off_x, self.off_y)

	def set_offset(self, x, y):
		self.off_x = x
		self.off_y = y

	def intersects(self, x, y):
		if x >= self.off_x and x < self.off_x + self.inner_width and y >= self.off_y and y < self.off_y + self.inner_height:
			dx = x - self.off_x
			dy = y - self.off_y

			return self.loc_mat[dx][dy] == 1

		return False

	def get_rotation(self):
		return self.rotation

	def get_block_type(self):
		return block_types[self.t]

	def c_rotate(self, board):
		return self.rotate(board, True)

	def cc_rotate(self, board):
		return self.rotate(board, False)

	def rotate(self, board, clockwise):
		if clockwise:
			self.rot = self.rot + 1 if self.rot < 3 else 0
			new_mat = [[self.loc_mat[x][y] for x in range(self.inner_width)] for y in range(self.inner_height-1, -1, -1)]
		else:
			self.rot = self.rot - 1 if self.rot > 0 else 3
			new_mat = [[self.loc_mat[x][y] for x in range(self.inner_width-1,-1,-1)] for y in range(self.inner_height)]

		new_width = len(new_mat)
		new_height = len(new_mat[0])

		if self.collides(board):
			return False

		self.loc_mat = new_mat
		self.inner_width = new_width
		self.inner_height = new_height

		return True

	def l_translate(self, board):
		return self.move(board, -1)

	def r_translate(self, board):
		return self.move(board, 1)

	def d_translate(self, board):
		if not self.collides(board, 0, 1):
			self.off_y += 1
			return True

		return False

	def drop(self, board):
		while self.d_translate(board):
			pass

	def collides(self, b, dx=0, dy=0):
		for ix in range(self.inner_width):
			for iy in range(self.inner_height):

				if self.loc_mat[ix][iy] == 0:
					continue

				x = self.off_x + ix
				y = self.off_y + iy

				if not b.in_bounds(x + dx, y + dy) or not b.is_empty(x + dx, y + dy):
					return True

		return False

	def move(self, b, dx=0, dy=0):
		if not self.collides(b, dx, dy):
			self.off_x += dx
			self.off_y += dy

			return True

		return False

	def has_clear_overhead(self, b):

		for ix in range(self.inner_width):
			for iy in range(self.inner_height):

				if self.loc_mat[ix][iy] == 0:
					continue

				x = self.off_x + ix
				y = self.off_y + iy

				dy = y - 1
				while not b.in_bounds(x, dy):
					if not b.is_empty(x,dy):
						return False

					dy -= 1

		return True

	def execute_move(self, move, board):
		move_dict = [
			self.c_rotate,
			self.cc_rotate,
			self.l_translate,
			self.r_translate,
			self.d_translate,
			self.drop
		]

		move_dict[move](board)

	def valid_rotations(self):
		return valid_rotations(self.type)

	def get_color(self):
		return block_color(self.t)

	def get_copy(self, r=0):
		return Block(self.t, r)

	def __str__(self):
		return self.get_block_type()
