# Tetris seven sequence piece generator
# Random Generator generates a sequence of all seven one-sided tetrominoes 
# (I, J, L, O, S, T, Z) permuted randomly, as if they were drawn from a bag. 
# Then it deals all seven tetrominoes to the piece sequence before generating another bag.

from random import shuffle
from utils import dequeue

class Piece_Generator:
	def __init__(self):
		self.bag = []

	def get_next(self):

		if len(self.bag) == 0:
			b = [i for i in range(7)]
			shuffle(b)
			self.bag = b

		return dequeue(self.bag)

