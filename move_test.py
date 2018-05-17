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
#'''
c = 5
t = Tree_node(format_bmat(b), c, -1, [])

t.generate_children()


# for c in t.get_children():
# 	c.print_node()

'''
board = format_bmat(b)
t_block = Block(5)
t_block.set_rotation(board,3)
t_block.set_offset(1,17)
print("----------")
print(t_block.set_rotation(board,0))
t_block.set(board)
print(board)
'''
