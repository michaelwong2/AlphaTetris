# tests for calculate moves

from api.bmat import Board_Matrix
from api.block import Block
from api.utils import encode_move, decode_move
from tree_components import calculate_move

# test 1
m1 = [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, 1], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, 1], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 4, 4], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 4, 4], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 2, 3], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 3], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 5, 5, 5], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, 1, 1], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, 1, 1], 
	  [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]

t1 = Board_Matrix()
t1.set_matrix(m1)
p1 = Block(1)
p1.set_offset(0,16)

print(calculate_move(t1, p1))
print("Answer: [0, 2, 2, 2, 5]")