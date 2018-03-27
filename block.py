# Block class

from random import randint

block_types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

# initialize a Block object with type (int, 0-6) and rotation (int, 0-3) and position (list)
# or don't include any arguments for a random block with random rotation and default position
class Block:
	def __init__(self, t=None, r=None, b=None):
		self.t = t if t != None else randint(0,6)
		self.rot = r if r != None else randint(0,3)
		self.occupied = s if s != None else spawns[self.t]
		self.board = b
		self.is_set = False

	def set(self):
		self.is_set = True

	def get_type(self):
		return self.t

	def get_occupied(self):
		return self.occupied

	def get_rotation(self):
		return self.rotation

	def get_block_type(self):
		return block_types[self.t]

	def crotate(self):
		self.rot = self.rot + 1 if self.rot < 3 else 0

	def ccrotate(self):
		self.rot = self.rot - 1 if self.rot > 0 else 3

	def to_string(self):
		return self.get_block_type()

	

