from gym_go import gogame
import numpy as np
from copy import deepcopy


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

    for i in range(1, len(board)):
        if board[0, i] == 1:
            if board[0, i - 1] == 0:
                groups += 1
        if board[i, 0] == 1:
            if board[i - 1, 0] == 0:
                groups += 1

    for i in range(1, len(board)):
        for j in range(1, len(board)):
            if board[i, j] == 1:
                if board[i - 1, j] == 0 and board[i, j - 1] == 0:
                    groups += 1

    return groups


def stones(state, color):
    black, white, _, _, _, _ = state
    board = []
    _stones = 0

    if color == 'b':
        board = black
    else:
        board = white

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i, j] == 1:
                _stones += 1

    return _stones


"""
Returns capture coordinates for given color
Currently returns first possible capture seen
Possible upgrade: find all possible captures for given state, return most profitable capture coordinates
"""


def checkForCapture(env, state, boardsize, color):
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
                state1, reward, done, info = testEnv.step((i, j))
                if stones(state1, gettingAttacked) < stoneCount:
                    # print(f"capture move: ({i},{j})")
                    env.render()
                    return i, j
    return -1, -1


def distance_to_stone(state, pos):
    """
    Returns color, -1 for white, 0 for both and 1 for black. And the distance
    """
    black, white, _, _, _, _ = state
    y, x = pos
    found = False
    b = False;
    w = False;
    if black[y, x] == 1:
        return 1, 0
    if white[y, x] == 1:
        return -1, 0
    dist = 0
    while not found or dist > len(black):
        dist += 1
        for i in range(-dist, dist + 1):
            if y + i >= 0:
                for j in range(-dist, dist + 1):
                    if x + i >= 0:
                        try:
                            if black[y + i, x + j] == 1:
                                b = True
                            if white[y + i, x + j] == 1:
                                w = True
                        except:
                            break
                        finally:
                            if b and w:
                                break
            if b and w:
                break
        if b or w:
            found = True
    score = -1 * w + b
    return score, dist
