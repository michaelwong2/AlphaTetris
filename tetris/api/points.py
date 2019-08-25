
def pointsFromLinesCleared(linesCleared, comboSoFar:int, tSpinType:int, isTetris:bool, isPerfectClear:bool, isB2BTetris:bool):
    linesSent = 0
    tSpinBonus = 2

    if linesCleared > 0:
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

    linesSent += lines

    if isTetris:
        linesSent += 2
        if isB2BTetris:
            linesSent += 4
            tSpinBonus = 3

    if tSpinType == 0:
        linesSent += tSpinBonus
    elif tSpinType == 1:
        linesSent += 2*tSpinBonus
    elif tSpinType == 2:
        linesSent += 3*tSpinBonus

    if isPerfectClear:
        linesSent += 10

    return linesSent