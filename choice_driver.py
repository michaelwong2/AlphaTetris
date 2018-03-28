# AI choice driver

ninf = float('-inf')

# returns list of integers representing best move
def make_choice(board, piece, held_piece, policy):
	policy.update(board)

	piece_perms = argmax_neighbor(board, piece, policy.rank)

	if piece.get_type() == held_piece.get_type():
		hpiece_perms = argmax_neighbor(board, held_piece, policy.rank)

		if piece_perms[0] < hpiece_perms[0]:
			return [0] + hpiece_perms[1]

	return piece_perms[1]

# finds the best ranked neighboring state according to a ranker
# returns tuple -> (rank: 0-1, moveset[])
def argmax_neighbor(board, piece, rank):
	 seen = {}

	 max_rank = ninf
	 best_moves = []

	 for rotation in range(4):

	 	# TODO: generate permutation as new_state and new piece location as npiece

	 	h = new_state.hash()
	 	if h in seen:
	 		del new_state
	 		continue

	 	r = rank(new_state)

	 	if r > max_rank:
	 		max_rank = r
	 		best_moves = generate_moveset(board, piece, npiece, rotation)

	 return (max_rank, best_moves)

# generate the move encoding for a state transition 
# returns int list
def generate_moveset(board, piece, new_piece, rotation):
	# if hard drop is available
	if new_piece.clear_overhead():
		# translate piece
		# rotate
		# drop
		# return move
	else: 
		# pathfind
		# translate
		# rotate
		# set?



