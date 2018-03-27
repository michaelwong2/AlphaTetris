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

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def hash(self):
		h = ''
		for x in range(self.width):
			for y in range(self.height):

				i = self.mat[x][y]

				if i != None: 
					h += i.to_string()

			h += 'a' 

		return h

	def get_copy(self):
		c = [[self.mat[x][y] for y in range(self.height)] for x in range(self.width)]
		return Board_Matrix(self.width, self.height, c)


