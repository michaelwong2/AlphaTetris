# Block class

from random import randint
import math

#The t ATTRIBUTE of each block is initialized to INDEX one of these
block_types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

#The loc_mat ATTRIBUTE of each block is initialized to be one of these
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

#order for clockwise rotations
rot_translations = [
	[(-1,1),(2,-1),(-2,2),(1,-2)],

	[(0,0),(1,0),(-1,1),(0,-1)],

	[(0,0),(1,0),(-1,1),(0,-1)],

	[(0,0),(0,0),(0,0),(0,0)],

	[(0,0),(1,0),(-1,1),(0,-1)],

	[(0,0),(1,0),(-1,1),(0,-1)],

	[(0,0),(1,0),(-1,1),(0,-1)]
]

#Number of unique rotations for each block type
vrots = [2,4,4,1,2,4,2]

#colors matching the block types
colors = [
	(31,185,253),
	(24,73,196),
	(255,120,10),
	(240,182,45),
	(130,209,65),
	(212,44,155),
	(248,58,93)
]

#@pre: block type
#@post: block color
def block_color(t):
	if t <= -1:
		return
	else:
		return colors[t]

def valid_rotations(t):
	return vrots[t]

# initialize a Block object with a board, a type (int, 0-6), rotation (int, 0-3) and offset (tuple x,y)
# or only include the board for a random block with default rotation and default position
class Block:
	def __init__(self, t=None):

		self.t = t if t != None else randint(0,6)
		self.rot = 0

		self.loc_mat = block_mats[self.t]
		self.rot_trans = rot_translations[self.t]

		self.inner_width = len(self.loc_mat)
		self.inner_height = len(self.loc_mat[0])

		self.set_offset(self.get_spawn())

	#@post: set a piece on the board. Piece's location defined by its offset
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

	#@post: perform a rotation (can be more than 1 clockwise step)
	def set_rotation(self, board, rotation):

		spin = self.c_rotate if rotation > self.rot else self.cc_rotate

		for i in range(abs(rotation - self.rot)):
			if not spin(board):
				return False

		# print("new rot: " + str(rotation))
		# print("old rot: " + str(self.rot))

		return True

	def get_rot_trans(self,rotation):
		return self.rot_trans[rotation]

	#@post: get x-coordinate of the piece's spawn location/offset
	def get_spawn(self, width=10):
		return math.floor(width / 2) - math.ceil(self.inner_width/2)

	def get_type(self):
		return self.t

	def get_width(self):
		return len(self.loc_mat)

	def get_height(self):
		return len(self.loc_mat[0])

	#@post: get current location of the piece
	def get_offset(self):
		return (self.off_x, self.off_y)

	#@post: set current location of the piece
	def set_offset(self, x, y=0):
		self.off_x = x
		self.off_y = y

	#@post: given (x,y), return True if the coordinates intersect with part of the piece
	def intersects(self, x, y):
		if x >= self.off_x and x < self.off_x + self.inner_width and y >= self.off_y and y < self.off_y + self.inner_height:
			dx = x - self.off_x
			dy = y - self.off_y

			return self.loc_mat[dx][dy] == 1

		return False

	def get_rotation(self):
		return self.rot

	def get_block_type(self):
		return block_types[self.t]

	def c_rotate(self, board):
		return self.rotate(board, True)

	def cc_rotate(self, board):
		return self.rotate(board, False)

	#@post: rotate the piece 1 step
	def rotate(self, board, clockwise):
		if clockwise:
			rot = self.rot + 1 if self.rot < 3 else 0
			new_mat = [[self.loc_mat[x][y] for x in range(self.inner_width)] for y in range(self.inner_height-1, -1, -1)]
		else:
			rot = self.rot - 1 if self.rot > 0 else 3
			new_mat = [[self.loc_mat[x][y] for x in range(self.inner_width-1,-1,-1)] for y in range(self.inner_height)]

		new_width = len(new_mat)
		new_height = len(new_mat[0])
		board_w = board.get_width()
		board_h = board.get_height()

		#find possible new offset (x,y)
		rot_trans = self.get_rot_trans(rot)
		new_off_x = self.off_x + rot_trans[0]
		new_off_y = self.off_y + rot_trans[1]
		if new_off_x < 0:
			new_off_x = 0
		elif new_off_x + new_width >= board_w:
			new_off_x = board_w - new_width

		#handle Wall Kick
		#move offset around if needed
		wall_kick = self.rot_collides(board,new_mat,new_width,new_height,new_off_x,new_off_y)
		if wall_kick == 1:
			new_off_x += 1
		elif wall_kick == -1:
			new_off_x -= 1

		if new_off_x + new_width >= board_w:
			new_off_x = board_w - new_width
		if self.rot_collides(board,new_mat,new_width,new_height,new_off_x,new_off_y) != 0:
			return False

		self.off_x = new_off_x
		self.off_y = new_off_y

		self.loc_mat = new_mat
		self.rot = rot
		self.inner_width = new_width
		self.inner_height = new_height

		return True

	#@post: return 0 if it's possible to fit this new rotation
	# return a positive integer indicating how much right the piece needs to move
	# return a negative integer indicating how much left the piece needs to move
	def rot_collides(self, board, new_mat, new_width, new_height, new_off_x, new_off_y):
		#move = 0
		#move_left = True
		for ix in range(new_width):
			for iy in range(new_height):

				if new_mat[ix][iy] == 0:
					continue

				x = new_off_x + ix
				y = new_off_y + iy

				if not board.is_empty(x,y):
					if ix == 0:
						return 1
					else:
						return -1

		return 0

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
		d = 0

		while self.d_translate(board):
			d += 1

		return d		

	#@post: return True if there's something at distance (dx,dy) from the piece
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

	def execute_moves(self, moves, board):
		for move in moves:
			self.execute_move(move, board)

	def valid_rotations(self):
		return valid_rotations(self.type)

	def get_color(self):
		return block_color(self.t)

	def get_copy(self, r=0):
		return Block(self.t, r)

	def __str__(self):
		return self.get_block_type()
