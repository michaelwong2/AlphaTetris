#testing utilities

from api.bmat import Board_Matrix

# [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def next_points(combo, lines, mode):
	sent_lines = 0
	if combo < 0:
		sent_lines = lines - 1
	elif (combo < 2 and mode == 'friends') or (combo < 1 and mode == 'battle'):
		sent_lines = lines
	elif (combo < 5 and mode == 'friends') or (combo < 3 and mode == 'battle'):
		sent_lines = lines + 1
	elif combo < 1 and mode == 'battle':
		sent_lines = lines + 2
	elif (combo < 7 and mode == 'friends') or (combo < 7 and mode == 'battle'):
		sent_lines = lines + 3
	elif (combo < 12 and mode == 'friends') or (combo > 6 and mode == 'battle'):
		sent_lines = lines + 4
	elif mode == 'friends':
		sent_lines = lines + 5
	return sent_lines

def format_bmat(matrix):

	b = Board_Matrix()

	for y in range(len(matrix)):
		for x in range(len(matrix[0])):
			v = matrix[y][x]

			if v == 0:
				v = None

			b.set(x, y, v)

	return b
