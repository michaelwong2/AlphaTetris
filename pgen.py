# Tetris seven sequence piece generator
# Random Generator generates a sequence of all seven one-sided tetrominoes 
# (I, J, L, O, S, T, Z) permuted randomly, as if they were drawn from a bag. 
# Then it deals all seven tetrominoes to the piece sequence before generating another bag.

from random import shuffle

class Piece_Generator:
	def __init__(self):
		self.bag = []
		self.fill_bag()

	def fill_bag(self):
		self.bag = [i for i in range(7)]
		shuffle(self.bag)

	def get_next(self):
		np = self.bag[0]
		del self.bag[0]

		if len(self.bag) == 0:
			self.fill_bag()

		return np
