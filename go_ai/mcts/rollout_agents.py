# An agent is a function which tries to evaluate the strength of a given state. It should return negative 
# values if it thinks white leads, 0 if it is a tie and positive values when black side is in the lead
from gym_go import gogame
from go_ai.mcts import utils

def rand_agent(state, komi, settings):
    """
    Creates random moves until the game is done and returns the winner. 
    
    Parameters:
    - state
    - komi
    - settings[0]: How many times a random sequence should be played
    """
    score = 0

    for _ in range(settings[0]):
        current_rollout_state = state

        while not gogame.game_ended(current_rollout_state):
            action = gogame.random_action(current_rollout_state)
            current_rollout_state = gogame.next_state(current_rollout_state, action)

        score += gogame.winning(current_rollout_state, komi)

    return score / settings[0]

def score_agent(state, komi, settings):
    """
    Checks score in current state. Aggressive.

    Parameters:
    - state
    - komi
    - settings (not used)
    """
    b, w = gogame.areas(state)
    return b - w - komi

def lib_agent(state, komi, settings):
    """
    Checks for liberties in current state. Passive.

    Parameters:
    - state
    - komi (not used)
    - settings[0]: str:color
    """
    libb, libw = gogame.liberties(state)
    board = []

    if settings[0] == 'b':
        board = libb
    else:
        board = libw

    if len(settings) == 1:
        settings.append(1)
        settings.append(1)

    _groups = utils.groups(state, settings[0])

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

def extended_lib_agent(state, komi, settings):
    """
    Parameters:
    - state
    - komi
    - settings[0]: str:color
    - settings[1]: modifier to liberties
    - settings[2]: groups
    - settings[3]: stones
    """
    if settings[0] == 'b':
        return lib_agent(state, komi, settings) + (utils.stones(state, settings[0])*settings[3])
    else:
        return lib_agent(state, komi, settings) - (utils.stones(state, settings[0])*settings[3])

