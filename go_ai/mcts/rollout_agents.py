# An agent is a function which tries to evaluate the strength of a given state. It should return - values
# if it thinks white leads, 0 if it thinks it is a tie and positive values for black leads
from gym_go import gogame
from go_ai.mcts import go_utils


# Creates random moves until the game is done and returns the winner. Settings[0] is how many times a random
# sequence should be played
def rand_agent(state, komi, settings):
    score = 0
    for i in range(settings[0]):
        current_rollout_state = state
        while not gogame.game_ended(current_rollout_state):
            action = gogame.random_action(current_rollout_state)
            current_rollout_state = gogame.next_state(current_rollout_state, action)
        score += gogame.winning(current_rollout_state, komi)
    return score / settings[0]


# Checks the score in the state
# Creates an aggresive AI which struggles with keeping groups alive
def score_agent(state, komi, settings):
    b, w = gogame.areas(state)
    return b - w - komi


def lib_agent(state, komi, settings):
    libb, libw = gogame.liberties(state)
    board = []
    if settings[0] == 'b':
        board = libb
    else:
        board = libw
    if len(settings) == 1:
        settings.append(1)
        settings.append(1)
    _groups = go_utils.groups(state, settings[0])
    libs = 0
    for i in board:
        for j in i:
            if j:
                libs += 1
    if _groups == 0:
        _groups = 1
    if settings[0] == 'b':
        return (libs * settings[1]) / (_groups * settings[2])
    else:
        return -((libs * settings[1]) / (_groups * settings[2]))


# settings[0] is which color the agent is, [1] modifier to liberties, [2] groups and [3] stones
def extended_lib_agent(state, komi, settings):
    if settings[0] == 'b':
        return lib_agent(state, komi, settings) + (go_utils.stones(state, settings[0])*settings[3])
    else:
        return lib_agent(state, komi, settings) - (go_utils.stones(state, settings[0])*settings[3])

