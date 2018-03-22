# Block class

import random

block_types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

# initialize a Block object with type (int, 0-6) and rotation (int, 0-3)
# or don't include any arguments for a random block with random rotation
class Block:
	def __init__(self, t=None, r=None):
		self.t = t if t != None else block_types[random.randint(0,6)]
		self.rot = r if r != None else random.randint(0,3)

	def get_type(self):
		return self.t

	def get_rotation(self):
		return self.rotation

	def get_block_type(self):
		return block_types[self.type]

