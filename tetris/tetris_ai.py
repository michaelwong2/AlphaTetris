# tetris ai test

import time
from tree_search import Tetris_Search_Tree
from api.utils import decode_move, encode_move, Piece_Generator
from copy import deepcopy
from api.bmat import Board_Matrix

board = Board_Matrix()
pg = Piece_Generator()

t = Tetris_Search_Tree(board=board, initial_pieces=[pg.get_next() for _ in range(3)])
moves = []

for i in range(600):

	t.enqueue(pg.get_next())
	if t.next_moves() == -1:
		break

	print("\033c")
	print("Time:", 600 - i)
	print("Lines sent:", t.root.lines_sent)
	print("Combo", t.root.combos_so_far)
	print("Hold:", "None" if t.root.held == -1 else t.root.held)
	print(t.root.board)

	time.sleep(0.01)

print("\033c")
print("Final lines:", t.root.lines_sent)
