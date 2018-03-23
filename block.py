# Block class

from random import randint

block_types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

spawns = [
	[(2,0),(3,0),(4,0),(5,0)],
	[],
	[],
	[(4,0),(5,0),(4,1),(5,1)],
	[],
	[],
	[]
]

# initialize a Block object with type (int, 0-6) and rotation (int, 0-3) and position (list)
# or don't include any arguments for a random block with random rotation and default position
class Block:
	def __init__(self, t=None, r=None, s=None, b=None):
		self.t = t if t != None else randint(0,6)
		self.rot = r if r != None else randint(0,3)
		self.occupied = s if s != None else spawns[self.t]
		self.board = b

	def get_type(self):
		return self.t

	def get_occupied(self):
		return self.occupied

	def get_rotation(self):
		return self.rotation

	def get_block_type(self):
		return block_types[self.t]

	def crotate(self):
		if self.board != None:
			print 'dad'

		self.rot = self.rot + 1 if self.rot < 3 else 0

	def ccrotate(self):
		if self.board != None:
			print 'dad'

		self.rot = self.rot - 1 if self.rot > 0 else 3

	def check_landed(self):
		if self.board == None:
			return
		
		# check if there is no more down movement

	def move_left(self):
		if self.board == None:
			return

		# check bounds
		for o in self.occupied:
			if o[0] == 0 or self.board[o[0] - 1][o[1]] != self:
				return

		for i in range(4):
			o = self.occupied[i]
			self.occupied[i] = (o[0] - 1, o[1])

	def move_right(self):
		if self.board == None:
			return

		# check bounds
		for o in self.occupied:
			if o[0] == 9 or self.board[o[0] + 1][o[1]] != self:
				return

		for i in range(4):
			o = self.occupied[i]
			self.occupied[i] = (o[0] + 1, o[1])

	def move_down(self):
		if not self.check_landed():
			for i in range(4):
				o = self.occupied[i]
				self.occupied[i] = (o[0], o[1] + 1)

	

