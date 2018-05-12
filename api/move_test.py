# tests for calculate moves

from api.bmat import Board_Matrix
from api.block import Block
from api.utils import encode_move, decode_move
from tree_components import calculate_move
from test_utils import format_bmat

# test 1
m = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 5, 4, 4, 1, 0, 1, 0, 0, 0], 
[0, 4, 0, 1, 4, 0, 1, 0, 0, 1], 
[0, 3, 0, 1, 4, 1, 1, 0, 0, 1], 
[0, 2, 0, 1, 3, 1, 3, 4, 4, 1], 
[0, 1, 1, 1, 2, 1, 2, 4, 3, 1]]

t1 = format_bmat(m)
p1 = Block(1)
p1.set_offset(0,16)

print(calculate_move(t1, p1))
print("Answer: [0, 2, 2, 2, 5]")