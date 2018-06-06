# utils

from random import shuffle

# given a list l, return the first element in it and remove it from the list
def dequeue(l):
	if l == None or len(l) == 0:
		return None
	else: 
		r = l[0]
		del l[0]
		return r

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


inf = float('inf')

def inf():
	return inf

def neg_inf():
	return -inf

class Piece_Generator:
	def __init__(self):
		self.bag = []

	def get_next(self):

		if len(self.bag) == 0:
			b = [i for i in range(7)]
			shuffle(b)
			self.bag = b

		return dequeue(self.bag)
