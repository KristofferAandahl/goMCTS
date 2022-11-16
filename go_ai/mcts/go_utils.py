# TODO: support for non 5*5 boards
def groups(state, color):
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


# TODO: support for non 5*5 boards
def stones(state, color):
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
