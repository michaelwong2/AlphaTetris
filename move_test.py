# tests for calculate moves

from api.bmat import Board_Matrix
from api.block import Block
from api.utils import encode_move, decode_move
from tree_components import Tree_node
from test_utils import format_bmat
from Ranker import Ranker


b= [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[1, 0, 0, 0, 0, 0, 1, 1, 0, 0], 
	[1, 0, 0, 1, 0, 0, 0, 1, 1, 1], 
	[0, 0, 0, 1, 1, 0, 1, 1, 1, 1]]

c = 5
board = format_bmat(b)
t = Tree_node(format_bmat(b), c, -1, [])

t.generate_children()

for d in t.get_children():
	d.print_node()

# a = Block(0)
# print("w:" , a.get_width(), " h: ", a.get_height())
# a.set_rotation(Board_Matrix(), 1)
# print("w:", a.get_width(), " h: ", a.get_height())
