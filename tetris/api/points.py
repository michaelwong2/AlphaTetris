#Regular Combos

# tspins
# 0 -- single
# 1 -- double
# 2 -- triple

def next_points(combo, lines, tetris, tspin, perf, b2b):

    sent_lines = 0

    if lines > 0:
        if combo < 0:
            sent_lines = -1-3
        elif combo < 2:
            sent_lines = 0-3
        elif combo < 5:
            sent_lines = 1-3
        elif combo < 7:
            sent_lines = 3-3
        elif combo < 12:
            sent_lines = 4-3
        else:
            sent_lines = 5-3

    sent_lines += lines

    if tetris and b2b:
        sent_lines += 6
    elif tetris:
        sent_lines += 4

    x = 2
    if b2b:
        x = 3
    if tspin == 0:
        sent_lines += x
    elif tspin == 1:
        sent_lines += 2*x
    elif tspin == 2:
        sent_lines += 3*x

    if perf:
        sent_lines += 10

    return sent_lines

#Perfect Clears
def perf_clear_detect(board):
    for x in range(board.get_width()):
        if not board.is_empty(x, 19):
            return False
    return True

#T-Spin Points
def tspin_detect(moves):
    last_index = len(moves)-1
    return moves[last_index] == 0 or moves[last_index] == 1

print(next_points(5, 0, False, 0, False, False))
