# Board matrix

class Board_Matrix:
	def __init__(self, w, h, b=[]):
		self.width = w
		self.height = h

		self.mat = b if len(b) > 0 else [[None for y in range(h)] for x in range(w)]

	def lookup(self, x, y):
		return self.mat[x][y]

	def set(self, x, y, item):
		self.mat[x][y] = item

	def is_empty(self, x, y):
		return self.mat[x][y] == None

	def clear(self):
		for x in range(self.width):
			for y in range(self.height):
				self.mat[x][y] = None

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def in_bounds(self, x, y):
		return x >= 0 and y >= 0 and x < self.width and y < self.height

	def hash(self):
		h = ''
		for x in range(self.width):
			for y in range(self.height):

				i = self.mat[x][y]

				h += 'p' if i == None else 'n'

			h += 'b' 

		return h

	# get a copy of the instance
	def get_copy(self):
		c = [[self.mat[x][y] for y in range(self.height)] for x in range(self.width)]
		return Board_Matrix(self.width, self.height, c)

	# if there are any complete lines, remove them
	def clear_lines(self):
		lines_cleared = 0

		for y in range(self.height):
			c = 0

			for x in range(self.width):	
				c += 1 if self.mat[x][y] != None else 0

			if c == self.width:
				self.shift_down(y)
				lines_cleared += 1

		return lines_cleared

	# shift down all cells (excluding live pieces) from i upwards
	def shift_down(self, i):

		if i >= self.height:
			print("oops")
			return

		for y in range(i-1, -1, -1):
			for x in range(self.width):
				self.mat[x][y+1] = self.mat[x][y]



