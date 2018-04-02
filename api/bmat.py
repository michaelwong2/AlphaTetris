# Board matrix

class Board_Matrix:
	def __init__(self, w, h, b=[], g=0):
		self.width = w
		self.height = h

		self.mat = b if len(b) > 0 else [[None for y in range(h)] for x in range(w)]

		self.gray_lines = g

	def lookup(self, x, y):
		return self.mat[x][y]

	def set(self, x, y, item):
		self.mat[x][y] = item

	def is_empty(self, x, y):
		return self.mat[x][y] == None

	def is_gray(self, x, y):
		return self.mat[x][y] == -1

	def clear(self):
		for x in range(self.width):
			for y in range(self.height):
				self.set(x,y,None)

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def set_grays(self,g):
		self.gray_lines = g

	def in_bounds(self, x, y):
		return x >= 0 and y >= 0 and x < self.width and y < self.height

	def hash(self):
		h = ''
		for x in range(self.width):
			for y in range(self.height):

				i = self.lookup(x,y)

				h += 'p' if i == None else 'n'

			h += 'b' 

		return h

	# get a copy of the instance
	def get_copy(self):
		c = [[self.lookup(x,y) for y in range(self.height)] for x in range(self.width)]
		return Board_Matrix(self.width, self.height, c, self.gray_lines)

	# add n gray lines to the bottom
	def add_grays(self, n):
		if self.shift_up(n):
			for y in range(self.height-1, self.height - n, -1):
				for x in range(self.width):
					self.set(x,y,-1)

			self.gray_lines += n
			return True

		return False

	# remove n gray lines
	def remove_grays(self, n):
		if gray_lines < n:
			return

		for i in range(n, -1, -1):
			self.shift_down(self.height - i - 1)

		gray_lines -= n

	# if there are any complete lines, remove them
	def clear_lines(self):
		lines_cleared = 0

		for y in range(self.height):
			c = 0

			for x in range(self.width):	
				c += 1 if self.is_empty(x,y) or self.is_gray(x,y) else 0

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
				self.set(x,y+1, self.lookup(x,y))

	# shift up all cells k <= n times
	# returns true if successful
	def shift_up(self, n):

		for i in range(n):
			for x in range(self.width):
				if not self.is_empty(x, 0):
					return False

			for y in range(self.height-2, -1, -1):
				for x in range(self.width):
					self.set(x,y, self.lookup(x,y+1))

		return True


