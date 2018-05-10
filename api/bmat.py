# Board matrix

class Board_Matrix:
	def __init__(self, w=10, h=20, b=[], g=0):
		self.width = w
		self.height = h

		self.mat = b if len(b) > 0 else [[None for y in range(h)] for x in range(w)]

		self.gray_lines = g

		self.bheight = 0 if len(b) == 0 else self.calc_build_height()

	def lookup(self, x, y):
		return self.mat[x][y]

	def set(self, x, y, item):
		self.mat[x][y] = item

		if item != None and item >= 0:
			n = self.height - y
			self.bheight = self.bheight if n < self.bheight else n

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

	def build_height(self):
		return self.bheight

	def calc_build_height(self):
		for y in range(self.height):
			for x in range(self.width):
				if not self.is_empty(x, y):
					return self.height - y

		return 0

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
			self.set(x,self.height-1, None)
			return True

		return False

	# add n = len(gaps) lines given an array of gaps of indeces
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

	# shift down all cells (excluding live pieces) from i upwards
	def shift_down(self, i):

		if i >= self.height:
			print("oops")
			return

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
