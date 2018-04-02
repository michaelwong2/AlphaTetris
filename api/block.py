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

# initialize a Block object with a board, a type (int, 0-6), rotation (int, 0-3) and offset (tuple x,y)
# or only include the board for a random block with default rotation and default position
class Block:
	def __init__(self, b, t=None, r=None, o=None):

		self.t = t if t != None else randint(0,6)
		self.rot = r if r != None else 0

		self.loc_mat = block_mats[self.t]

		self.inner_width = len(self.loc_mat)
		self.inner_height = len(self.loc_mat[0])

		self.board = b

		self.reset_offset()

	def set(self):
		for x in range(self.inner_width):
			for y in range(self.inner_height):
				if self.loc_mat[x][y] == 1:
					self.board.set(self.off_x + x, self.off_y + y, self.t)

	def get_type(self):
		return self.t

	def get_offset(self):
		return (self.off_x, self.off_y)

	def set_offset(self, x, y):
		self.off_x = x
		self.off_y = y

	def set_board(self, b):
		self.board = b

	def reset_offset(self):
		self.set_offset(math.floor(self.board.get_width() / 2) - math.ceil(self.inner_width/2), 0)

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

	def c_rotate(self):
		return self.rotate(True)

	def cc_rotate(self):
		return self.rotate(False)

	def rotate(self, clockwise):
		if clockwise:
			self.rot = self.rot + 1 if self.rot < 3 else 0
			new_mat = [[self.loc_mat[x][y] for x in range(self.inner_width)] for y in range(self.inner_height-1, -1, -1)]
		else:
			self.rot = self.rot - 1 if self.rot > 0 else 3
			new_mat = [[self.loc_mat[x][y] for x in range(self.inner_width-1,-1,-1)] for y in range(self.inner_height)]

		new_width = len(new_mat)
		new_height = len(new_mat[0])

		if self.collides(0,0):
			return False

		self.loc_mat = new_mat
		self.inner_width = new_width
		self.inner_height = new_height	

		return True	

	def l_translate(self):
		return self.move(-1, 0)

	def r_translate(self):
		return self.move(1, 0)

	def d_translate(self):
		if not self.collides(0,1):
			self.off_y += 1
			return True

		return False

	def drop(self):
		while self.d_translate():
			pass

	def collides(self, dx, dy):
		b = self.board

		for ix in range(self.inner_width):
			for iy in range(self.inner_height):

				if self.loc_mat[ix][iy] == 0:
					continue

				x = self.off_x + ix
				y = self.off_y + iy

				if not b.in_bounds(x + dx, y + dy) or not b.is_empty(x + dx, y + dy):
					return True

		return False

	def move(self, dx, dy):
		if not self.collides(dx, dy):
			self.off_x += dx
			self.off_y += dy

			return True

		return False

	def has_clear_overhead(self):
		b = self.board

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

	def execute_move(self, move):
		move_dict = [
			self.c_rotate,
			self.cc_rotate,
			self.l_translate,
			self.r_translate,
			self.d_translate,
			self.drop
		]

		move_dict[move]()

	def valid_rotations(self):
		return vrots[self.t]

	def get_color(self):
		return block_color(self.t)

	def get_copy(self):
		return Block(self.board, self.t)

	def __str__(self):
		return self.get_block_type()


	

