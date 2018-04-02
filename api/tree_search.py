# Tree Searching algorithm

# return 2-tuple with move array and ranking
# (moveset[], rank: 0-1)
def recurse_with_successor_states(board, current_piece, held_piece, piece_queue, rank):
	pass

# return 2-tuple with move array and ranking
# (moveset[], rank: 0-1)
def recursive_state_tree_DFS(board, current_piece, held_piece, piece_queue, rank):
	
	move_with_child = recurse_with_successor_states(board, current_piece, held_piece, piece_queue, rank)
	move_with_held = recurse_with_successor_states(board, held_piece, current_piece, piece_queue, rank)

	if move_with_child[1] > move_with_held[1]:
		return move_with_child
	else:
		return ([encode_move('hold')] + move_with_held[0], move_with_held[1])