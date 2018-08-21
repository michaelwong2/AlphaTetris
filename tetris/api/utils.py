# utils

from random import shuffle
from collections import deque

move_int_map = {
	'crot': 0,
	'ccrot': 1,
	'left': 2,
	'right': 3,
	'down': 4,
	'drop': 5,
	'hold': 6
}

int_move_map = ['crot', 'ccrot', 'left', 'right', 'down', 'drop', 'hold']

def encode_move(m):
	en = move_int_map.get(m)
	return -1 if en == None else en

def decode_move(m):
	return 'error' if m >= 7 else int_move_map[m]

def valid_moves():
	return int_move_map

# Bag algorithm
class Piece_Generator:
	def __init__(self):
		self.bag = deque()

	def get_next(self):

		if len(self.bag) == 0:
			b = [i for i in range(7)]
			shuffle(b)
			self.bag = deque(b)

		return self.bag.popleft()
