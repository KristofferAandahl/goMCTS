from copy import deepcopy

def groups(state, color):
    # TODO: Support non 5*5 boards
    groups = 0
    black, white, _, _, _, _ = state
    board = []

    if color == 'b':
        board = black
    else:
        board = white
    
    if board[0, 0] == 1:
        groups += 1

    for i in range(1, 5):
        if board[0, i] == 1:
            if board[0, i - 1] == 0:
                groups += 1
        if board[i, 0] == 1:
            if board[i - 1, 0] == 0:
                groups += 1

    for i in range(1, 5):
        for j in range(1, 5):
            if board[i, j] == 1:
                if board[i - 1, j] == 0 and board[i, j - 1] == 0:
                    groups += 1

    return groups

def stones(state, color):
    # TODO: Support non 5*5 boards
    black, white, _, _, _, _ = state
    board = []
    _stones = 0

    if color == 'b':
        board = black
    else:
        board = white

    for i in range(5):
        for j in range(5):
            if board[i, j] == 1:
                _stones += 1

    return _stones

def checkForCapture(env, state, boardsize, color):
    """
    Returns capture coordinates for given color.
    Currently returns first possible capture seen.
    """
    # TODO: Possible upgrade: find all possible captures for given state, return most profitable capture coordinates
    if color == 'w':
        stoneCount = stones(state, 'b')
        gettingAttacked = 'b'
    else:
        stoneCount = stones(state, 'w')
        gettingAttacked = 'w'

    for i in range(boardsize):
        for j in range(boardsize):
                testEnv = deepcopy(env)
                if state[3][i][j] != 1:
                    state1, _, _, _ = testEnv.step((i,j))
                    if stones(state1, gettingAttacked) < stoneCount:
                        env.render()
                        return i,j
    return -1,-1
