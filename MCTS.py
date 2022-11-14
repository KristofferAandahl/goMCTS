import numpy as np
from collections import defaultdict
import gym
from gym_go import gogame


class MonteCarloTreeSearchNode():
    def __init__(self, state, komi, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self.komi = komi
        return

    def untried_actions(self):
        self._untried_actions = list(gogame.valid_moves(self.state))
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = gogame.random_action(self.state)
        while self._untried_actions[action] == 0:
            action = gogame.random_action(self.state)

        self._untried_actions[action] = 0
        next_state = gogame.next_state(self.state, action)
        child_node = MonteCarloTreeSearchNode(
            next_state, self.komi, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return gogame.game_ended(self.state)

    def rollout(self):
        current_rollout_state = self.state

        while not gogame.game_ended(current_rollout_state):
            action = gogame.random_action(current_rollout_state)
            current_rollout_state = gogame.next_state(current_rollout_state, action)
        return gogame.winning(current_rollout_state, self.komi)

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        expand = 0
        for i in self._untried_actions:
            expand += i
        return expand == 0

    def best_child(self, c_param=0.1):

        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self):
        possible_moves = gogame.valid_moves(self.state)
        r = np.random.randint(len(possible_moves))
        while possible_moves(r) == 0:
            r = np.random.randint(len(possible_moves))
        return r

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)


def move(state):
    root = MonteCarloTreeSearchNode(state, 0)
    selected_node = root.best_action()
    return selected_node


go_env = gym.make('gym_go:go-v0', size=5, komi=0, reward_method='real')
go_env.reset()

state, reward, done, info = go_env.step((1, 1))

while done == False:
    state, reward, done, info = go_env.step(move(state).parent_action)

go_env.render('human')