# An agent is a function which tries to evaluate the strength of a given state. It should return - values
# if it thinks white leads, 0 if it thinks it is a tie and positive values for black leads
from gym_go import gogame
import gym
import numpy as np

import go_utils


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


# settings[0] is which color the agent is
def lib_agent(state, komi, settings):
    libb, libw = gogame.liberties(state)
    board = []
    if settings[0] == 'b':
        board = libb
    else:
        board = libw
    _groups = go_utils.groups(state, settings[0])
    libs = 0
    for i in board:
        for j in i:
            if j:
                libs += 1
    if _groups == 0:
        _groups = 1
    if settings[0] == 'b':
        return (libs / _groups) + go_utils.stones(state, settings[0])
    else:
        return (-libs / _groups) - go_utils.stones(state, settings[0])

