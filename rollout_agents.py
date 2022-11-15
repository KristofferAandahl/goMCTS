# An agent is a function which tries to evaluate the strength of a given state. It should return - values
# if it thinks white leads, 0 if it thinks it is a tie and positive values for black leads
from gym_go import gogame
import gym
import numpy as np


# Creates random moves until the game is done and returns the winner
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
