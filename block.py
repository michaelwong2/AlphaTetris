# Block class

from random import randint

block_types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

spawns = [
	[]
]

rotations = []

# initialize a Block object with type (int, 0-6) and rotation (int, 0-3) and position (list)
# or don't include any arguments for a random block with random rotation and default position
class Block:
	def __init__(self, b, t=None, r=None, o=None):

		self.t = t if t != None else randint(0,6)
		self.rot = r if r != None else rotations[self.t]
		self.occupied = o if o != None else spawns[self.t]

		self.board = b

	def set(self):
		# remove all pointers to this object so that it can be garbage collected
		for x,y in self.occupied:
			self.board.set(x,y,self.t)

	def get_type(self):
		return self.t

	def get_occupied(self):
		return self.occupied

	def set_occupied(self, positions):
		self.occupied = positions

	def get_rotation(self):
		return self.rotation

	def get_block_type(self):
		return block_types[self.t]

	def c_rotate(self):
		self.rot = self.rot + 1 if self.rot < 3 else 0

	def cc_rotate(self):
		self.rot = self.rot - 1 if self.rot > 0 else 3

	def l_translate(self):
		return self.move(-1, 0)

	def r_translate(self):
		return self.move(1, 0)

	def d_translate(self):
		return self.move(0, 1)

	def drop(self):
		move = True
		while move:
			move = d_translate(self)

	def move(self, dx, dy):
		b = self.board

		for x,y in self.occupied:
			if not b.in_bounds(x + dx, y + dy):
				return False

			target = b.lookup(x + dx, y + dy)
			if target != None and target is not self:
				return False

		i = 0
		for x,y in self.occupied:
			b.set(x, y, None)
			b.set(x + dx, y + dy, self)
			self.occupied[i] = (x + dx, y + dy)
			i += 1

		return True

	def clear_overhead(self):
		b = self.board

		for x,y in self.occupied:
			dy = y - 1

			while not b.in_bounds(x, dy):
				t = b.lookup(x, dy)

				if t != None and t is not self:
					return False
					
				dy -= 1

		return True

	def to_string(self):
		return self.get_block_type()

	

